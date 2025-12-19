from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello from Customer Service!"})

if __name__ == '__main__':
    app.run(port=5004, debug=True)
