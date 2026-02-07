# Prediction routes
from flask import Blueprint, request, jsonify
from utils.model_runner import run_prediction

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")

@predict_bp.route("/", methods=["POST"])
def predict():
    data = request.json
    symbol = data.get("symbol")
    prediction = run_prediction(symbol)
    return jsonify(prediction)