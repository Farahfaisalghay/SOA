# from flask import Flask, request, jsonify
# import datetime
# import uuid
# import requests

# app = Flask(__name__)


# @app.route('/api/orders/create', methods=['POST'])
# def create_order():
#  # 1. Receive JSON data from the JSP application [cite: 42, 59]
#         data = request.get_json()
#         try:

#             # 2. Validate input parameters
#             customer_id = data.get('customer_id')
#             products = data.get('products')   # [{"product_id": 1, "quantity": 2}]
#             total_amount = data.get('total_amount')

#             if not customer_id or not products:
#                 return jsonify({"error": "Missing customer_id or products"}), 400

#             # Check inventory BEFORE order confirmation
#             inventory_response = requests.post(
#                 "http://localhost:5002/api/inventory/validate",
#                 json={"products": products}
#             )

#             if inventory_response.status_code != 200:
#                 return jsonify({
#                     "status": "Failed",
#                     "message": "Inventory validation failed",
#                     "details": inventory_response.json()
#                 }), 400

#             #  3. Generate unique order ID and timestamp [cite: 46]
        
#             order_id = str(uuid.uuid4())
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             # Update inventory after order 
        
#             for item in products:
#                 requests.put(
#                     "http://localhost:5002/api/inventory/update",
#                     json={
#                         "product_id": item["product_id"],
#                         "quantity": item["quantity"]
#                     }
#                 )

#         # 4. Return order confirmation status [cite: 47]
#             return jsonify({
#                 "status": "Success",
#                 "order_id": order_id,
#                 "timestamp": timestamp,
#                 "message": f"Order created successfully for customer {customer_id}"
#             }), 201

#         except Exception as e:
#             return jsonify({"error": str(e)}), 500


#     # Endpoint to retrieve order details [cite: 50]
# @app.route('/api/orders/<order_id>', methods=['GET'])
# def get_order(order_id):
#         return jsonify({
#             "order_id": order_id,
#             "details": "Order details retrieval logic goes here"
#         })
#     # --------------------------------------------------
# if __name__ == '__main__':
#         app.run(port=5001, debug=True)
        
        
        
from flask import Flask, request, jsonify
import datetime
import uuid
import requests

app = Flask(__name__)

@app.route('/api/orders/create', methods=['POST'])
def create_order():
    # 1. Receive JSON data from the JSP application
    data = request.get_json()
    try:
        # 2. Validate input parameters
        customer_id = data.get('customer_id')
        products = data.get('products')   # [{"product_id": 1, "quantity": 2}]
        region = data.get('region', 'default')  # Get region for tax calculation
        total_amount = data.get('total_amount')
        
        if not customer_id or not products:
            return jsonify({"error": "Missing customer_id or products"}), 400
        
        # Check inventory BEFORE order confirmation
        inventory_response = requests.post(
            "http://localhost:5002/api/inventory/validate",
            json={"products": products}
        )
        
        if inventory_response.status_code != 200:
            return jsonify({
                "status": "Failed",
                "message": "Inventory validation failed",
                "details": inventory_response.json()
            }), 400
        
        # NEW: Call Pricing Service to get detailed pricing breakdown
        try:
            pricing_response = requests.post(
                "http://localhost:5003/api/pricing/calculate",
                json={"products": products, "region": region},
                timeout=5
            )
            
            if pricing_response.status_code == 200:
                pricing_data = pricing_response.json()
                # Use calculated grand_total from Pricing Service
                total_amount = pricing_data.get('grand_total', total_amount)
            else:
                # If pricing service fails, continue with provided total_amount
                pricing_data = None
                print(f"Warning: Pricing service returned {pricing_response.status_code}")
                
        except requests.RequestException as e:
            # If pricing service is unavailable, continue without it
            pricing_data = None
            print(f"Warning: Could not connect to Pricing Service: {e}")
        
        # 3. Generate unique order ID and timestamp
        order_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update inventory after order 
        for item in products:
            requests.put(
                "http://localhost:5002/api/inventory/update",
                json={
                    "product_id": item["product_id"],
                    "quantity": item["quantity"]
                }
            )
        
        # 4. Return order confirmation status with pricing breakdown
        response_data = {
            "status": "success",
            "order_id": order_id,
            "customer_id": customer_id,
            "timestamp": timestamp,
            "message": f"Order created successfully for customer {customer_id}"
        }
        
        # Add pricing data if available
        if pricing_data:
            response_data["pricing"] = pricing_data
        else:
            # Fallback: basic pricing info if Pricing Service unavailable
            response_data["total_amount"] = total_amount
        
        return jsonify(response_data), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve order details
@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    return jsonify({
        "order_id": order_id,
        "details": "Order details retrieval logic goes here"
    })

# --------------------------------------------------
if __name__ == '__main__':
    app.run(port=5001, debug=True)