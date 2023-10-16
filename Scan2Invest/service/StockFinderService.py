import requests
from exceptions import ServiceExceptions

class StockFinderService:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_endpoint = "https://www.alphavantage.co/query"
       
    def lookup_stock_info(self, symbol):
        try:   

            #  url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    # response = requests.get(url)
    # # Ensure to navigate through actual API response to fetch price
    # return response.json()["Global Quote"]["05. price"]
            # finnhub_client = finnhub.Client(api_key=self.api_key)
            params = {"function": 'GLOBAL_QUOTE', "symbol": symbol,"apikey": self.api_key}

            response = requests.get(self.api_endpoint, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "API Request Failed", "message": f"Status Code: {response.status_code}"}

        except Exception as e:
            print(f"Error in stock finder {e}")
            raise ServiceExceptions.ServiceError(f"Error retrieving ticker information: {str(e)}")
    
    def lookup_symbol(self, name):
        try:

            if not isinstance(name, str):
                raise ValueError("Name must be a string.")
            # https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo

            params = {"function": 'SYMBOL_SEARCH', "keywords": name,"apikey": self.api_key}
                        
            response = requests.get(self.api_endpoint, params=params)
            if response.status_code == 200:
                return response.json()['bestMatches']
            else:
                return {"error": "API Symbol Lookupt Request Failed", "message": f"Status Code: {response.status_code}"}
        except Exception as e:
            print(f"Error in stock finder {e}")
            raise ServiceExceptions.ServiceError(f"Error retrieving symbol information: {str(e)}")
        
    def build_possible_investment(self, company_keyword, top_n=3):
        try:
            best_matches = self.lookup_symbol(company_keyword)
            ivestment_json = {
                    "company": best_matches[0]["2. name"],
                    "investment_options": []
                }
            
            for match in best_matches[:top_n]:  
                stock_info = self.lookup_stock_info(match["1. symbol"])
                stock_price = stock_info["Global Quote"]["05. price"]
                investment_option = {
                    "type": match["3. type"],
                    "symbol": match["1. symbol"],
                    "stock_price": stock_price,
                    "region": match["4. region"]
                }
                ivestment_json["investment_options"].append(investment_option)

            return ivestment_json
        except Exception as e:
            print(f"Error building possible investments {e}")
            raise ServiceExceptions.ServiceError(f"Error retrieving possible investment information: {str(e)}")
        

