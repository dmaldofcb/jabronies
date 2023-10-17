from flask import Blueprint, jsonify, request
from Scan2Invest.service.StockFinderService import StockFinderService
from Scan2Invest.service.ImageDetectionService import ImageDetectionService
from Scan2Invest.service.ProcessImageService import ProcessImageService
from Scan2Invest.exceptions.ServiceExceptions import ServiceError
import json
from Scan2Invest.config import ConfigManager

# Create a Blueprint
scan_2_invest_bp = Blueprint('scan_2_invest', __name__)

GOOGLE_API_KEY = ConfigManager.GOOGLE_API

VANTAGE_API_KEY = ConfigManager.ALPHA_VANTAGE_API

@scan_2_invest_bp.route("/")
def home():
    print("Welcome to Scan2Invest!")
    return '<h1>Welcome to Scan2Invest API</h1>'

@scan_2_invest_bp.route("/possibleinvestment", methods=['POST'])
def build_investment():
    try:
        data = request.get_json()
        keyword = data.get('keyword') 

        if not keyword:
            return jsonify(error='No keyword was sent'), 400
        
        print(f"Sending the Ticker: {keyword}")

        stock_price_service = StockFinderService(VANTAGE_API_KEY)
        response = stock_price_service.build_possible_investment(keyword)
        return jsonify(response), 200
    except Exception as e:
        print(str(e))
        # Return a 500 error to the client with the error message from the service
        return jsonify(error="Stock Finder API Error", message=str(e)), 500

@scan_2_invest_bp.route("/stockinformation", methods=['POST'])
def stock_finder():
    try:
        data = request.get_json()
        ticker = data.get('ticker') 

        if not ticker:
            return jsonify(error='No ticker was sent'), 400
        
        print(f"Sending the Ticker: {ticker}")

        stock_price_service = StockFinderService(VANTAGE_API_KEY)
        response = stock_price_service.lookup_stock_info(ticker)
        return jsonify(response), 200
    except Exception as e:
        print(str(e))
        # Return a 500 error to the client with the error message from the service
        return jsonify(error="Stock Finder API Error", message=str(e)), 500

@scan_2_invest_bp.route("/searchsymbols", methods=['POST'])
def symbol_finder():
    try:
        data = request.get_json()
        symbol = data.get('symbol') 

        if not symbol:
            return jsonify(error='No ticker was sent'), 400
        
        print(f"Sending the Symbol: {symbol}")
        
        stock_price_service = StockFinderService(VANTAGE_API_KEY)
        response = stock_price_service.lookup_symbol(symbol)
        return response, 200
    except Exception as e:
        print(str(e))
        # Return a 500 error to the client with the error message from the service
        return jsonify(error="Symbol Finder API Error", message=str(e)), 500

@scan_2_invest_bp.route("/upload_image", methods=['POST'])
def upload_image():

    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400

    try: 
        # Preprocess the image sent
        process_image_service = ProcessImageService()
        preprocessed_filepath = process_image_service.preprocess_image(file)

        #Use google Vision to try to find best possible brand
        image_detection_service = ImageDetectionService(GOOGLE_API_KEY)
        image_response = image_detection_service.send_to_vision_api(preprocessed_filepath)
        brand_name = image_detection_service.extract_logo_description(image_response)

        if brand_name is None:
            return jsonify(error='Could not identify brand name from image'), 401
        
        print(f"Possible Brand Name of product: {brand_name}")

        #Build the possible investments based on the brand name
        stock_price_service = StockFinderService(VANTAGE_API_KEY)
        response = stock_price_service.build_possible_investment(brand_name)
        print(json.dumps(response, indent=4))

        response["brand_name_detected"] = brand_name
        response["image_file_name"] = file.filename
        
        return jsonify(response), 200
    
    except ServiceError as e:
        print(str(e))
        # Return a 500 error to the client with the error message from the service
        return jsonify(error="Upload Image API Failure", message=str(e)), 500
    except Exception as e:
        print(str(e))
        # Return a 500 error to the client with the error message from the service
        return jsonify(error="Internal Server Error", message=str(e)), 500
    
