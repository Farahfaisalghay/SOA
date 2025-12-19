# from flask import Flask, request, jsonify
# import mysql.connector
# import requests

# app = Flask(__name__)

# # ---------- Database Configuration ----------
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "Secret123!",
#     "database": "ecommerce_system"
# }

# # ---------- Helper: DB Connection ----------
# def get_db_connection():
#     return mysql.connector.connect(**DB_CONFIG)

# # ---------- Test Endpoint ----------
# @app.route("/")
# def home():
#     return jsonify({"message": "Hello from Pricing Service!"})

# # ---------- Pricing Calculation Endpoint ----------
# @app.route("/api/pricing/calculate", methods=["POST"])
# def calculate_price():
#     try:
#         data = request.get_json()
#         products = data.get("products", [])

#         if not products:
#             return jsonify({"error": "No products provided"}), 400

#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         total = 0.0
#         breakdown = []

#         for item in products:
#             product_id = item["product_id"]
#             quantity = item["quantity"]

#             # 1️⃣ Get base price from Inventory Service
#             inv_response = requests.get(
#                 f"http://localhost:5002/api/inventory/check/{product_id}"
#             )

#             if inv_response.status_code != 200:
#                 return jsonify({"error": f"Product {product_id} not found"}), 404

#             product_data = inv_response.json()
#             unit_price = product_data["unit_price"]

#             subtotal = unit_price * quantity
#             discount = 0.0

#             # 2️⃣ Check discount rules
#             cursor.execute(
#                 """
#                 SELECT discount_percentage
#                 FROM pricing_rules
#                 WHERE product_id = %s AND %s >= min_quantity
#                 """,
#                 (product_id, quantity)
#             )

#             rule = cursor.fetchone()
#             if rule:
#                 discount = subtotal * (rule["discount_percentage"] / 100)

#             final_price = subtotal - discount
#             total += final_price

#             breakdown.append({
#                 "product_id": product_id,
#                 "unit_price": unit_price,
#                 "quantity": quantity,
#                 "subtotal": subtotal,
#                 "discount": discount,
#                 "final_price": final_price
#             })

#         # 3️⃣ Apply tax
#         cursor.execute("SELECT tax_rate FROM tax_rates WHERE region = 'default'")
#         tax_row = cursor.fetchone()
#         tax_rate = tax_row["tax_rate"] if tax_row else 0

#         tax_amount = total * (tax_rate / 100)
#         grand_total = total + tax_amount

#         cursor.close()
#         conn.close()

#         return jsonify({
#             "items": breakdown,
#             "total_before_tax": total,
#             "tax_rate": tax_rate,
#             "tax_amount": tax_amount,
#             "grand_total": grand_total
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(port=5003, debug=True)
from flask import Flask, request, jsonify
import mysql.connector
import requests

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Use your MySQL username
    'password': 'Secret123!',  # Use your MySQL password
    'database': 'myprojectdb'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/api/pricing/calculate', methods=['POST'])
def calculate_pricing():
    """
    Calculate final pricing for an order
    Receives: {"products": [{"product_id": 1, "quantity": 2}]}
    Returns: Itemized pricing breakdown with discounts and totals
    """
    try:
        # 1. Get product data from request
        data = request.get_json()
        products = data.get('products')
        region = data.get('region', 'default')  # Optional region for tax calculation
        
        if not products or not isinstance(products, list):
            return jsonify({"error": "Invalid or missing products data"}), 400
        
        # 2. Initialize pricing breakdown
        pricing_breakdown = {
            "items": [],
            "subtotal": 0.0,
            "total_discount": 0.0,
            "tax": 0.0,
            "grand_total": 0.0
        }
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # 3. Process each product
        for product in products:
            product_id = product.get('product_id')
            quantity = product.get('quantity', 1)
            
            if not product_id:
                continue
            
            # 4. Get base price from Inventory Service
            try:
                inventory_response = requests.get(
                    f"http://localhost:5002/api/inventory/check/{product_id}",
                    timeout=5
                )
                
                if inventory_response.status_code != 200:
                    return jsonify({
                        "error": f"Failed to fetch price for product {product_id}"
                    }), 500
                
                inventory_data = inventory_response.json()
                base_price = float(inventory_data.get('unit_price', 0))
                product_name = inventory_data.get('product_name', f'Product {product_id}')
                
            except requests.RequestException as e:
                return jsonify({
                    "error": f"Could not connect to Inventory Service: {str(e)}"
                }), 500
            
            # 5. Calculate line total
            line_total = base_price * quantity
            
            # 6. Check for applicable discounts from database
            cursor.execute("""
                SELECT discount_percentage 
                FROM pricing_rules 
                WHERE product_id = %s AND min_quantity <= %s
                ORDER BY discount_percentage DESC
                LIMIT 1
            """, (product_id, quantity))
            
            discount_row = cursor.fetchone()
            discount_percentage = float(discount_row['discount_percentage']) if discount_row else 0.0
            discount_amount = (line_total * discount_percentage) / 100
            final_price = line_total - discount_amount
            
            # 7. Add to breakdown
            pricing_breakdown['items'].append({
                "product_id": product_id,
                "product_name": product_name,
                "quantity": quantity,
                "unit_price": base_price,
                "line_total": round(line_total, 2),
                "discount_percentage": discount_percentage,
                "discount_amount": round(discount_amount, 2),
                "final_price": round(final_price, 2)
            })
            
            pricing_breakdown['subtotal'] += line_total
            pricing_breakdown['total_discount'] += discount_amount
        
        # 8. Calculate tax from database
        cursor.execute("""
            SELECT tax_rate 
            FROM tax_rates 
            WHERE region = %s
        """, (region,))
        
        tax_row = cursor.fetchone()
        tax_rate = float(tax_row['tax_rate']) if tax_row else 0.0
        
        subtotal_after_discount = pricing_breakdown['subtotal'] - pricing_breakdown['total_discount']
        tax_amount = (subtotal_after_discount * tax_rate) / 100
        
        pricing_breakdown['tax_rate'] = tax_rate
        pricing_breakdown['tax'] = round(tax_amount, 2)
        pricing_breakdown['subtotal'] = round(pricing_breakdown['subtotal'], 2)
        pricing_breakdown['total_discount'] = round(pricing_breakdown['total_discount'], 2)
        pricing_breakdown['grand_total'] = round(subtotal_after_discount + tax_amount, 2)
        
        cursor.close()
        conn.close()
        
        return jsonify(pricing_breakdown), 200
        
    except Exception as e:
        return jsonify({"error": f"Pricing calculation failed: {str(e)}"}), 500

@app.route('/api/pricing/rules/<int:product_id>', methods=['GET'])
def get_pricing_rules(product_id):
    """
    Get all pricing rules for a specific product
    """
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT rule_id, product_id, min_quantity, discount_percentage
            FROM pricing_rules
            WHERE product_id = %s
            ORDER BY min_quantity ASC
        """, (product_id,))
        
        rules = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({"product_id": product_id, "rules": rules}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pricing/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "Pricing Service is running", "port": 5003}), 200

if __name__ == '__main__':
    print("Starting Pricing Service on port 5003...")
    app.run(port=5003, debug=True)