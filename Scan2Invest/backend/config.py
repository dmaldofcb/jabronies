import os
from dotenv import load_dotenv

load_dotenv()

class ConfigManager:
    GOOGLE_API = os.environ.get('GOOGLE_API_KEY')
    ALPHA_VANTAGE_API = os.environ.get('VANTAGE_API_KEY')
        
    
