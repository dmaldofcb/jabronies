import base64
import requests
import json
import finnhub
from app.exceptions import ServiceExceptions

class StockFinderService:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_endpoint = "https://ticker-2e1ica8b9.now.sh/keyword/"
       
    def lookup_ticker(self, ticker):
        try:   
            finnhub_client = finnhub.Client(api_key=self.api_key)
            return (finnhub_client.quote(ticker))
        except Exception as e:
            print(f"Error in stock finder {e}")
            raise ServiceExceptions.ServiceError(f"Error retrieving ticker information: {str(e)}")
    
    def lookup_symbol(self, name):
        try:
            response = requests.get(
                url=f"{self.api_endpoint}{name}",
                headers={'Content-Type': 'application/json'}
            )
            print(json.dumps(response.json(), indent=4))
            #return response
        except Exception as e:
            print(f"Error in stock finder {e}")
            raise ServiceExceptions.ServiceError(f"Error retrieving symbol information: {str(e)}")

        if response.status_code == 200:
            return response.json()
        else:
            return response.text

