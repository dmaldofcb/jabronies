from flask import Flask
from app.controller import scan_2_invest
from app import create_app

app = create_app()
app = Flask(__name__)
app.register_blueprint(scan_2_invest.scan_2_invest_bp)

if __name__ == "__main__":
    # Developement with debug run
    # app.run(host='0.0.0.0', port=5000, debug=True)
    
    #Cloud run
    app.run()
