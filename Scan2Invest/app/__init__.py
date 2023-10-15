from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    # Importing and registering Blueprints
    from .controller.scan_2_invest import scan_2_invest_bp
    app.register_blueprint(scan_2_invest_bp)
    
    return app
