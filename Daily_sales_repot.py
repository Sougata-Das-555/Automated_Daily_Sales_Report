from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from datetime import datetime
import csv
import webbrowser
from threading import Timer

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = "Dail_sales_report.html"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# Built-in CORS support (no need to install flask-cors)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# Flask Setup, Basic routes, Take inputs

@app.route("/", methods=["GET"])
def home():
    if (BASE_DIR / HTML_FILE).exists():
        return send_from_directory(BASE_DIR, HTML_FILE)
    return jsonify({
        "error": f"'{HTML_FILE}' not found in {BASE_DIR}"
    }), 404


@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "success": True,
        "message": "Dail_sales_report.py backend is running!"
    })


@app.route("/download/<path:filename>", methods=["GET"])
def download_report(filename):
    return send_from_directory(REPORT_DIR, filename, as_attachment=True)


@app.route("/generate-report", methods=["POST", "OPTIONS"])
def generate_report():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON data"}), 400

        products = data.get("products")
        sold_data = data.get("soldData")

        if not isinstance(products, list) or not isinstance(sold_data, list):
            return jsonify({"error": "Invalid products or sales list"}), 400

        if not products:
            return jsonify({"error": "Add at least one product"}), 400

        product_map = {}

        for p in products:
            if not isinstance(p, dict):
                return jsonify({"error": "Invalid product record"}), 400

            for key in ("ID", "Name", "Price", "Quantity"):
                if key not in p:
                    return jsonify({"error": f"Missing product field: {key}"}), 400

            product_id = str(p["ID"]).strip()

            if not product_id or product_id in product_map:
                return jsonify({"error": "Product IDs must be unique and non-empty"}), 400

            try:
                price = float(p["Price"])
                quantity = int(p["Quantity"])
            except (ValueError, TypeError):
                return jsonify({"error": "Invalid price or stock quantity"}), 400

            if price < 0 or quantity < 0:
                return jsonify({"error": "Price and stock cannot be negative"}), 400

            p["ID"] = product_id
            p["Price"] = price
            p["InitialQuantity"] = quantity
            p["Quantity"] = quantity
            p["Sold"] = 0
            p["Total"] = round(price * quantity, 2)

            product_map[product_id] = p

        