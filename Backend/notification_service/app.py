from flask import Flask, request, jsonify
import requests
import datetime
import smtplib
import re
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Menna123?",          
        database="ecommerce_system"
    )

# validate email given
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# email sender
def send_real_email(to_email, subject, body):
    sender_email = "daliahasan397@gmail.com"
    app_password = "aipq cnvu trrq koos"  

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)


@app.route('/api/notifications/send', methods=['POST'])
def send_notification():
    try:
        # get the request and order details
        data = request.get_json()

        order_id = data.get("order_id")
        customer_id = data.get("customer_id")
        products = data.get("products")
        total_amount = data.get("total_amount")

        if not order_id or not customer_id or not products:
            return jsonify({"error": "Missing required data"}), 400

        # get custumer dtails from service
        customer_response = requests.get(
            f"http://localhost:5004/api/customers/{customer_id}"
        )

        if customer_response.status_code != 200:
            return jsonify({"error": "Failed to retrieve customer info"}), 400

        customer = customer_response.json()
        customer_name = customer.get("name")
        customer_email = customer.get("email")

        # estimate delivery time from inventory quantity
        delivery_info = ""
        for item in products:
            product_id = item["product_id"]

            inventory_response = requests.get(
                f"http://localhost:5002/api/inventory/check/{product_id}"
            )

            if inventory_response.status_code == 200:
                inv = inventory_response.json()
                qty = inv["quantity_available"]

                if qty > 15:
                    estimate = "Delivered in 2-3 days"
                elif qty > 0:
                    estimate = "Delivered in 5-7 days"
                else:
                    estimate = "Out of stock - delayed delivery"

                delivery_info += f"- Product {product_id}: {estimate}\n"
            else:
                delivery_info += f"- Product {product_id}: Delivery unavailable\n"

        # notification msg
        message = f"""
        Dear {customer_name},

        Your order has been successfully placed!

        Order ID: {order_id}

        Products:
        """
        for item in products:
            message += f"- Product {item['product_id']} | Quantity {item['quantity']}\n"

        message += f"""
        Total Amount: {total_amount} EGP

        Delivery Estimates:
        {delivery_info}
        see you again next time!
        """

        subject = f"Order Confirmation #{order_id}"

        # email
        if is_valid_email(customer_email):
            try:
                send_real_email(customer_email, subject, message)
                sent_via = "real email"
                print(f"EMAIL SENT TO: {customer_email}")
                print(message)

            except Exception:
                print("EMAIL FAILED — FALLBACK TO CONSOLE")
                print(message)
                sent_via = "console fallback"
        else:
            print("INVALID EMAIL — SIMULATION ONLY")
            print(message)
            sent_via = "console simulation"

        # log the notification to db
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO notification_log (order_id, customer_id, notification_type, message)
            VALUES (%s, %s, %s, %s)
            """,
            (
                order_id,
                customer_id,
                sent_via,
                message
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "Notification processed successfully",
            "sent_via": sent_via,
            "order_id": order_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5005, debug=True)
