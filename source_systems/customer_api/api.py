from flask import Flask, jsonify
from pathlib import Path
import json

app = Flask(__name__)

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "customer_data.json", "r") as file:
    customers = json.load(file)


@app.route("/customers", methods=["GET"])
def get_customers():
    return jsonify(customers)


if __name__ == "__main__":
    app.run(debug=True, port=5000)