from flask import Flask, request, jsonify
import datetime
import uuid

app = Flask(__name__)

@app.route('/api/orders/create', methods=['POST'])
def create_order():
    # 1. Receive JSON data from the JSP application [cite: 42, 59]
    data = request.get_json()
    
    try:
        # 2. Validate input parameters [cite: 45, 59]
        customer_id = data.get('customer_id')
        products = data.get('products') # Expected format: [{"product_id": 1, "quantity": 2}]
        total_amount = data.get('total_amount')

        if not customer_id or not products:
            return jsonify({"error": "Missing customer_id or products"}), 400

        # 3. Generate unique order ID and timestamp [cite: 46]
        order_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 4. Return order confirmation status [cite: 47]
        return jsonify({
            "status": "Success",
            "order_id": order_id,
            "timestamp": timestamp,
            "message": f"Order created successfully for customer {customer_id}"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve order details [cite: 50]
@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    return jsonify({
        "order_id": order_id,
        "details": "Order details retrieval logic goes here"
    })


if __name__ == '__main__':
    app.run(port=5001, debug=True)


