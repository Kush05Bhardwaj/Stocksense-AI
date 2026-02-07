# Portfolio management routes
from flask import Blueprint, request, jsonify
from portfolio.simulator import Portfolio

portfolio_bp = Blueprint("portfolio", __name__, url_prefix="/portfolio")
portfolio = Portfolio()

@portfolio_bp.route("/buy", methods=["POST"])
def buy_stock():
    data = request.json
    result = portfolio.buy_stock(
        symbol=data.get("symbol"),
        quantity=data.get("quantity"),
        price=data.get("price")
    )
    return jsonify({"message": "Stock bought successfully", "result": result})

@portfolio_bp.route("/status", methods=["GET"])
def status():
    return jsonify({
        "portfolio_value": portfolio.get_portfolio_value(),
        "holdings": portfolio.get_holdings(),
        "cash": portfolio.get_cash()
    })