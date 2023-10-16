from flask import Flask
from flask_cors import CORS
from Scan2Invest.controller.scan_2_invest import scan_2_invest_bp

app = Flask(__name__)
app.register_blueprint(scan_2_invest_bp)

CORS(app)

if __name__ == "__main__":
    # Developement with debug run
    # app.run(host='0.0.0.0', port=5000, debug=True)
    
    #Cloud run
    app.run()
