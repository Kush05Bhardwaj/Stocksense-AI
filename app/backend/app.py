from flask import Flask
from flask_cors import CORS
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.predict import predict_bp
from routes.sentiment import sentiment_bp
from routes.portfolio import portfolio_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(sentiment_bp, url_prefix='/api')
app.register_blueprint(portfolio_bp, url_prefix='/api')

@app.route('/')
def home():
    return {'message': 'StockSense AI API', 'status': 'running'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)