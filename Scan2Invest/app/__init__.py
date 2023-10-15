from flask import Flask
from app.controller import scan_2_invest

def create_app():
    app = Flask(__name__)
    # Importing and registering Blueprints
    app.register_blueprint(scan_2_invest.scan_2_invest_bp)
    
    return app
