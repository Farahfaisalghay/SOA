from flask import Flask, request, jsonify
import mysql.connector
import requests

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Menna123?",
        database="ecommerce_system"
    )

# ---------------- 1. GET CUSTOMER PROFILE ----------------
@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT customer_id, name, email, phone, loyalty_points, created_at "
        "FROM customers WHERE customer_id = %s",
        (customer_id,)
    )
    customer = cursor.fetchone()

    cursor.close()
    conn.close()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer), 200


# ---------------- 2. GET CUSTOMER ORDER HISTORY ----------------
@app.route('/api/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT customer_id FROM customers WHERE customer_id = %s",
        (customer_id,)
    )
    customer = cursor.fetchone()
    cursor.close()
    conn.close()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        order_service_url = (
            f"http://localhost:5001/api/orders?customer_id={customer_id}"
        )
        response = requests.get(order_service_url)

        if response.status_code != 200:
            return jsonify({"error": "Order Service error"}), 500

        orders = response.json()

    except Exception as e:
        return jsonify({"error": "Order Service not reachable"}), 500

    return jsonify({
        "customer_id": customer_id,
        "orders": orders
    }), 200


# ---------------- 3. UPDATE LOYALTY POINTS ----------------
@app.route('/api/customers/<int:customer_id>/loyalty', methods=['PUT'])
def update_loyalty(customer_id):
    data = request.get_json()

    if not data or "points" not in data:
        return jsonify({"error": "Missing points value"}), 400

    points = data["points"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT loyalty_points FROM customers WHERE customer_id = %s",
        (customer_id,)
    )
    customer = cursor.fetchone()

    if not customer:
        cursor.close()
        conn.close()
        return jsonify({"error": "Customer not found"}), 404

    cursor.execute(
        "UPDATE customers SET loyalty_points = loyalty_points + %s "
        "WHERE customer_id = %s",
        (points, customer_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Loyalty points updated",
        "added_points": points
    }), 200


# ---------------- RUN SERVICE ----------------
if __name__ == '__main__':
    app.run(port=5004, debug=True)
