from flask import Blueprint, request, jsonify
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.model_runner import run_prediction

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symbol = data.get('symbol', 'AAPL')
    model_type = data.get('model', 'xgb')
    
    try:
        result = run_prediction(symbol, model_type)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500