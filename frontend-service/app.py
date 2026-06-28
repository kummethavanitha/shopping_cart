"""
frontend-service
-----------------
Simple web UI. Calls catalog-service to show products + live prices,
and calls order-service to place an order. Lives in its own 'frontend'
namespace, talking to the other two namespaces over the network.
"""

import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

CATALOG_SERVICE_URL = os.environ.get(
    "CATALOG_SERVICE_URL",
    "http://catalog-service.catalog-pricing.svc.cluster.local:5001",
)
ORDER_SERVICE_URL = os.environ.get(
    "ORDER_SERVICE_URL",
    "http://order-service.orders.svc.cluster.local:5002",
)


@app.route("/health")
def health():
    return {"status": "ok", "service": "frontend"}


@app.route("/")
def index():
    try:
        resp = requests.get(f"{CATALOG_SERVICE_URL}/products", timeout=5)
        resp.raise_for_status()
        products = resp.json()
        error = None
    except requests.exceptions.RequestException as e:
        products = []
        error = f"Could not reach catalog-service: {e}"
    return render_template("index.html", products=products, error=error)


@app.route("/buy/<int:product_id>", methods=["POST"])
def buy(product_id):
    quantity = int(request.form.get("quantity", 1))
    try:
        resp = requests.post(
            f"{ORDER_SERVICE_URL}/orders",
            json={"product_id": product_id, "quantity": quantity},
            timeout=5,
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException:
        pass
    return redirect(url_for("orders"))


@app.route("/orders")
def orders():
    try:
        resp = requests.get(f"{ORDER_SERVICE_URL}/orders", timeout=5)
        resp.raise_for_status()
        order_list = resp.json()
        error = None
    except requests.exceptions.RequestException as e:
        order_list = []
        error = f"Could not reach order-service: {e}"
    return render_template("orders.html", orders=order_list, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
