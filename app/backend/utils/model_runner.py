import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import pandas as pd
import numpy as np
from models.prepare_data import create_features
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import yfinance as yf
from datetime import datetime, timedelta

def run_prediction(symbol, model_type='xgb'):
    """
    Run prediction for a given stock symbol
    """
    # Fetch fresh data for the requested symbol
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*5)  # 5 years of data
        
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            raise ValueError(f"No data found for symbol {symbol}")
        
        # Reset index to make Date a column
        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date'])
        
    except Exception as e:
        # Fallback to cached data if symbol fetch fails
        print(f"Error fetching {symbol}: {e}. Using cached data.")
        try:
            df = pd.read_csv('data/processed/data_with_sentiment.csv')
        except:
            df = pd.read_csv('data/processed/data.csv')
    
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