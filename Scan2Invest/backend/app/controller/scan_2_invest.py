from flask import Blueprint, jsonify, request
import os
import cv2

# Create a Blueprint
scan_2_invest_bp = Blueprint('scan_2_invest', __name__)

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

    # Ensure the directory exists
    save_dir = 'temp_image'
    os.makedirs(save_dir, exist_ok=True)
    
    # Ensure the directory exists
    save_processed_dir = 'processed_image'
    os.makedirs(save_processed_dir, exist_ok=True)
    
    # Save the file temporarily
    filepath = os.path.join(save_dir, file.filename)
    file.save(filepath)
    
    # Preprocess the image
    preprocessed_filepath = preprocess_image(filepath, save_processed_dir)

    
    # Dummy response
    response = {
        "company": "Example Corp.",
        "stock_price": 123.45,
        "investment_options": ["Stock", "Bond", "ETF"],
        "Image filepath": preprocessed_filepath
    }
    
    return jsonify(response)

def preprocess_image(image_path, save_processed):
    
    try:
        # Load and preprocess the image using OpenCV
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Save or return the preprocessed image
        preprocessed_path = 'preprocessed_' + os.path.basename(image_path)
        filepath = os.path.join(save_processed, preprocessed_path)
        print(f"Filepath {filepath}")
        cv2.imwrite(filepath, blurred)
    except Exception as e:
        print(f"Failed to Preprocess image error: {e}")
        return None    
    return preprocessed_path