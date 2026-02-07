# Portfolio management routes
from flask import Blueprint, request, jsonify
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from portfolio.simulator import Portfolio

portfolio_bp = Blueprint('portfolio', __name__)

# In-memory portfolio storage (use database in production)
portfolios = {}

@portfolio_bp.route('/portfolio/create', methods=['POST'])
def create_portfolio():
    data = request.json
    user_id = data.get('user_id', 'default')
    initial_balance = data.get('balance', 10000)
    
    portfolios[user_id] = Portfolio(initial_balance=initial_balance)
    
    return jsonify({'message': 'Portfolio created', 'balance': initial_balance}), 201

@portfolio_bp.route('/portfolio/<user_id>', methods=['GET'])
def get_portfolio(user_id):
    if user_id not in portfolios:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    portfolio = portfolios[user_id]
    return jsonify({
        'balance': portfolio.balance,
        'stocks': portfolio.stocks,
        'total_value': portfolio.get_total_value()
    }), 200