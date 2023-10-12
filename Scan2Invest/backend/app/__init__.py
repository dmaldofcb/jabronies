from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Importing and registering Blueprints
    from .controller.scan_2_invest import scan_2_invest_bp
    app.register_blueprint(scan_2_invest_bp)
    
    return app
