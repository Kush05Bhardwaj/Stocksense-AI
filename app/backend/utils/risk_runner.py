# Risk assessment utilities
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import pandas as pd
from risk.volatility import calculate_volatility
from risk.confidence import full_risk_assessment

def calculate_risk(symbol):
    """
    Calculate risk metrics for a given stock
    """
    # Load data
    df = pd.read_csv('data/processed/data.csv')
    prices = df['Close'].values
    
    # Calculate volatility
    volatility = calculate_volatility(prices, window=30)
    
    # Get full risk assessment
    risk_data = full_risk_assessment(prices)
    
    return {
        'symbol': symbol,
        'volatility': float(volatility),
        'risk_score': risk_data.get('risk_score', 0),
        'confidence_interval': risk_data.get('confidence_interval', [0, 0])
    }