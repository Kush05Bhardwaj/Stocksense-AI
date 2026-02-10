from flask import Blueprint, request, jsonify
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.model_runner import run_all_predictions

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symbol = data.get('symbol', 'AAPL')
    
    try:
        result = run_all_predictions(symbol)
        return jsonify(result), 200
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in prediction: {error_trace}")
        return jsonify({'error': str(e), 'trace': error_trace}), 500