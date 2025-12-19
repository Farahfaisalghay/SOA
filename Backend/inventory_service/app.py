from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="Secret123!",
    database="myprojectdb"
    )

#product availability
# GET /api/inventory/check/<product_id>
@app.route('/api/inventory/check/<int:product_id>', methods=['GET'])
def check_inventory(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) #json

    cursor.execute(
        "SELECT product_id, product_name, quantity_available, unit_price "
        "FROM inventory WHERE product_id = %s",
        (product_id,)
    )
#get one product i asked from db
    product = cursor.fetchone()
    cursor.close()
    conn.close()
#invalid
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200



# POST /api/inventory/validate
# validate that order does exist
@app.route('/api/inventory/validate', methods=['POST'])
def validate_inventory():
    data = request.get_json()

    try:
        products = data.get("products")

        if not products:
            return jsonify({"error": "No products provided"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        for item in products: #for every thing in order
            product_id = item["product_id"]
            quantity = item["quantity"]

            cursor.execute(
                "SELECT quantity_available FROM inventory WHERE product_id = %s",
                (product_id,)
            )
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": f"Product {product_id} not found"}), 404

            if result["quantity_available"] < quantity:
                return jsonify({
                    "error": f"low stock for product {product_id}"
                }), 400

        cursor.close()
        conn.close()

        return jsonify({"status": "Inventory available"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PUT /api/inventory/update
#after an order is done
@app.route('/api/inventory/update', methods=['PUT'])
def update_inventory():
    data = request.get_json()
    try:
        product_id = data["product_id"]
        quantity = data["quantity"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT quantity_available FROM inventory WHERE product_id = %s",
            (product_id,)
        )
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Product not found"}), 404

        if result[0] < quantity:
            return jsonify({"error": "low stockk"}), 400

        cursor.execute(
            "UPDATE inventory SET quantity_available = quantity_available - %s "
            "WHERE product_id = %s",
            (quantity, product_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Inventory updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# GET /api/inventory/products
@app.route('/api/inventory/products', methods=['GET'])
def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT product_id, product_name, quantity_available, unit_price "
        "FROM inventory"
    )
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(products), 200


# --------------------------------------------------
if __name__ == '__main__':
    app.run(port=5002, debug=True)