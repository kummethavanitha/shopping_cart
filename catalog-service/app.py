"""
catalog-service
---------------
Serves the product catalog (name + price) from products.json.

This file (products.json) is the file you edit + git push whenever
you want to change a price. Jenkins picks up the change, rebuilds
this service's image, and Kubernetes rolls out the update
automatically in the 'catalog-pricing' namespace.
"""

import json
import os
from flask import Flask, jsonify, abort

app = Flask(__name__)

DATA_FILE = os.environ.get(
    "PRODUCTS_FILE_PATH",
    os.path.join(os.path.dirname(__file__), "products.json"),
)


def load_products():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "catalog-service"})


@app.route("/products")
def get_products():
    return jsonify(load_products())


@app.route("/products/<int:product_id>")
def get_product(product_id):
    products = load_products()
    for p in products:
        if p["id"] == product_id:
            return jsonify(p)
    abort(404, description="Product not found")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
