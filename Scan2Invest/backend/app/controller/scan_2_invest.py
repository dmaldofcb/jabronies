from flask import Blueprint, jsonify, request

# Create a Blueprint
scan_2_invest_bp = Blueprint('scan_2_invest', __name__)

@scan_2_invest_bp.route("/")
def home():
    return "Welcome to Scan2Invest!"

@scan_2_invest_bp.route("/upload_image", methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    
    # Dummy response
    response = {
        "company": "Example Corp.",
        "stock_price": 123.45,
        "investment_options": ["Stock", "Bond", "ETF"]
    }
    
    return jsonify(response)
