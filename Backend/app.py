from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Secret123!",
    database="myprojectdb"
)

@app.route("/test")
def test():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)