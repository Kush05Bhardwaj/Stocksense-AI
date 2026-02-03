# Flask Backend Application
from flask import Flask, request, jsonify
from routes.predict import predict_bp
from routes.sentiment import sentiment_bp
from routes.portfolio import portfolio_bp

app = Flask(__name__)
app.register_blueprint(predict_bp, url_prefix='/predict')
app.register_blueprint(sentiment_bp, url_prefix='/sentiment')
app.register_blueprint(portfolio_bp, url_prefix='/portfolio')

if __name__ == "__main__":
    app.run(debug=True)