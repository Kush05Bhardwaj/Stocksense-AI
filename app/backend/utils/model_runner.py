import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import pandas as pd
import numpy as np
from models.prepare_data import create_features
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

def run_prediction(symbol, model_type='xgb'):
    """
    Run prediction for a given stock symbol
    """
    # Load data
    df = pd.read_csv('data/processed/data.csv')
    
    # Try to load sentiment data
    try:
        df = pd.read_csv('data/processed/data_with_sentiment.csv')
    except:
        pass
    
    # Prepare features
    X, y = create_features(df, window=5)
    
    # Train model
    if model_type == 'xgb':
        model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
    else:
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    
    # Use 80% for training
    split = int(0.8 * len(X))
    X_train, y_train = X[:split], y[:split]
    
    model.fit(X_train, y_train)
    
    # Predict next value
    last_window = X[-1].reshape(1, -1)
    prediction = model.predict(last_window)[0]
    
    return {
        'symbol': symbol,
        'prediction': float(prediction),
        'current_price': float(df['Close'].iloc[-1]),
        'model': model_type
    }