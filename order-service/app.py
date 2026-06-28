"""
order-service
-------------
Accepts an order (product_id + quantity), fetches the CURRENT price
from catalog-service (running in a different namespace), and
calculates the total. This proves cross-namespace service
communication is working.
"""

import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Cross-namespace DNS: <service-name>.<namespace>.svc.cluster.local
CATALOG_SERVICE_URL = os.environ.get(
    "CATALOG_SERVICE_URL",
    "http://catalog-service.catalog-pricing.svc.cluster.local:5001",
)

orders_db = []
next_order_id = 1


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "order-service"})


@app.route("/orders", methods=["POST"])
def create_order():
    global next_order_id
    data = request.get_json(force=True)
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    try:
        resp = requests.get(f"{CATALOG_SERVICE_URL}/products/{product_id}", timeout=5)
        resp.raise_for_status()
        product = resp.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not reach catalog-service: {e}"}), 502

    total = round(product["price"] * quantity, 2)
    order = {
        "order_id": next_order_id,
        "product_id": product_id,
        "product_name": product["name"],
        "unit_price": product["price"],
        "quantity": quantity,
        "total": total,
    }
    orders_db.append(order)
    next_order_id += 1

    return jsonify(order), 201


@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(orders_db)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
