from flask import Blueprint, jsonify, request
import os
import cv2
from app.service.ImageDetectionService  import ImageDetectionService
from app.service.ProcessImageService import ProcessImageService
from app.exceptions import ServiceExceptions

# Create a Blueprint
scan_2_invest_bp = Blueprint('scan_2_invest', __name__)

GOOGLE_API_KEY = "AIzaSyAbsOeawghwfFOVNFmU8CQp8VzBTfYoH5w"

@scan_2_invest_bp.route("/")
def home():
    return "Welcome to Scan2Invest!"

@scan_2_invest_bp.route("/upload_image", methods=['POST'])
def upload_image():

    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400

    try: 
        # Preprocess the image
        process_image_service = ProcessImageService()
        preprocessed_filepath = process_image_service.preprocess_image(file)

        image_detection_service = ImageDetectionService(GOOGLE_API_KEY)
        image_response = image_detection_service.send_to_vision_api(preprocessed_filepath)
        brand_name = image_detection_service.extract_logo_description(image_response)
        
        # Dummy response
        response = {
            "company": brand_name,
            "stock_price": 123.45,
            "investment_options": ["Stock", "Bond", "ETF"],
            "Image Name": file.filename,
        }
        return jsonify(response), 200
    
    except ServiceExceptions.ServiceError as e:
        print(str(e))
        # Return a 500 error to the client with the error message from the service
        return jsonify(error="Upload Image Failure", message=str(e)), 500
    except Exception as e:
        print(str(e))
        # Return a 500 error to the client with the error message from the service
        return jsonify(error="Internal Server Error", message=str(e)), 500
    
