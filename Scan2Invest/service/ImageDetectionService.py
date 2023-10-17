import base64
import requests
import json
from Scan2Invest.exceptions.ServiceExceptions import ServiceError

class ImageDetectionService:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_endpoint = "https://vision.googleapis.com/v1/images:annotate"
        
    def extract_logo_description(self, api_response):
        try:
            logo_annotations = api_response['responses'][0]['logoAnnotations']
            return logo_annotations[0]['description']
        except (KeyError, IndexError, TypeError):
            print("Could not extract logo description from API response.")
            return None
    
    def encode_image(self, image_path):
        try: 
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Failed trying to base 64 encode the image error: {e}")
            return None
        return encoded_string
    
    def send_to_vision_api(self, image_path):
        # Encode the image
        encoded_image = self.encode_image(image_path)
        
        if encoded_image is None:
            print(f"No image could be Encoded returning")
            raise ServiceError(f"Invalid image could not encode")
        
        try:
            
            # Construct the JSON payload
            payload = {
                "requests": [
                    {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {
                            "type": "LOGO_DETECTION"
                        },
                    ]
                    }
                ]
            }
            
            
            # print request
            # print(json.dumps(payload, indent=4))
            # Send the request to the API
            response = requests.post(
                url=f"{self.api_endpoint}?key={self.api_key}",
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            
            # print response
            print(json.dumps(response.json(), indent=4))
        except Exception as e:
            print(f"Error in image detection {e}")
            raise ServiceError(f"Error Sending Image to Vision API: {str(e)}")
        
        # Handle the API response
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
