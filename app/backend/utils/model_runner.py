import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import pandas as pd
import numpy as np
from models.prepare_data import create_features
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import yfinance as yf
from datetime import datetime, timedelta

def get_currency_symbol(symbol):
    """
    Detect currency based on stock symbol suffix
    """
    currency_map = {
        '.NS': '₹',      # NSE India (National Stock Exchange)
        '.BO': '₹',      # BSE India (Bombay Stock Exchange)
        '.L': '£',       # London Stock Exchange
        '.TO': 'C$',     # Toronto Stock Exchange
        '.AX': 'A$',     # Australian Stock Exchange
        '.HK': 'HK$',    # Hong Kong Stock Exchange
        '.T': '¥',       # Tokyo Stock Exchange
        '.KS': '₩',      # Korea Stock Exchange
        '.SS': '¥',      # Shanghai Stock Exchange
        '.SZ': '¥',      # Shenzhen Stock Exchange
        '.SA': 'R$',     # Brazil Stock Exchange
        '.MC': '€',      # Madrid Stock Exchange
        '.PA': '€',      # Paris Stock Exchange
        '.DE': '€',      # Deutsche Börse
        '.MI': '€',      # Milan Stock Exchange
    }
    
    # Check for suffix
    for suffix, curr in currency_map.items():
        if symbol.upper().endswith(suffix):
            return curr
    
    # Default to USD for US stocks and unknown markets
    return '$'

def run_all_predictions(symbol):
    """
    Run predictions using ALL models and return results
    """
    stock = None
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
        stock = None
        try:
            df = pd.read_csv('data/processed/data_with_sentiment.csv')
        except:
            df = pd.read_csv('data/processed/data.csv')
    
    # Prepare features
    X, y = create_features(df, window=5)
    
    # Use 80% for training
    split = int(0.8 * len(X))
    X_train, y_train = X[:split], y[:split]
    
    # Get last window for prediction
    last_window = X[-1].reshape(1, -1)
    current_price = float(df['Close'].iloc[-1])
    
    predictions = []
    
    # 1. Linear Regression
    try:
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        lr_pred = lr_model.predict(last_window)[0]
        predictions.append({
            'model': 'Linear Regression',
            'prediction': float(lr_pred),
            'change': ((lr_pred - current_price) / current_price) * 100
        })
    except Exception as e:
        print(f"Linear Regression error: {e}")
    
    # 2. Random Forest
    try:
        rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        rf_model.fit(X_train, y_train)
        rf_pred = rf_model.predict(last_window)[0]
        predictions.append({
            'model': 'Random Forest',
            'prediction': float(rf_pred),
            'change': ((rf_pred - current_price) / current_price) * 100
        })
    except Exception as e:
        print(f"Random Forest error: {e}")
    
    # 3. XGBoost
    try:
        xgb_model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
        xgb_model.fit(X_train, y_train)
        xgb_pred = xgb_model.predict(last_window)[0]
        predictions.append({
            'model': 'XGBoost',
            'prediction': float(xgb_pred),
            'change': ((xgb_pred - current_price) / current_price) * 100
        })
    except Exception as e:
        print(f"XGBoost error: {e}")
    
    # 4. LSTM
    try:
        # Reshape data for LSTM [samples, time steps, features]
        X_train_lstm = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
        last_window_lstm = last_window.reshape((1, 1, last_window.shape[1]))
        
        lstm_model = Sequential([
            LSTM(50, activation='relu', input_shape=(1, X_train.shape[1])),
            Dropout(0.2),
            Dense(25, activation='relu'),
            Dense(1)
        ])
        lstm_model.compile(optimizer='adam', loss='mse')
        lstm_model.fit(X_train_lstm, y_train, epochs=10, batch_size=32, verbose=0)
        
        lstm_pred = lstm_model.predict(last_window_lstm, verbose=0)[0][0]
        predictions.append({
            'model': 'LSTM',
            'prediction': float(lstm_pred),
            'change': ((lstm_pred - current_price) / current_price) * 100
        })
    except Exception as e:
        print(f"LSTM error: {e}")
    
    # Get currency and company info
    currency = get_currency_symbol(symbol)
    company_name = symbol
    
    try:
        if stock:
            stock_info = stock.info
            company_name = stock_info.get('longName', symbol)
            currency_from_info = stock_info.get('currency', 'USD')
            
            # Map currency codes to symbols
            currency_symbols = {
                'USD': '$', 'INR': '₹', 'GBP': '£', 'EUR': '€',
                'JPY': '¥', 'CNY': '¥', 'HKD': 'HK$', 'CAD': 'C$',
                'AUD': 'A$', 'KRW': '₩', 'BRL': 'R$'
            }
            currency = currency_symbols.get(currency_from_info, currency)
    except Exception as e:
        print(f"Error getting company info: {e}")
    
    return {
        'symbol': symbol,
        'company_name': company_name,
        'current_price': current_price,
        'currency': currency,
        'predictions': predictions
    }

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
    
    # Get currency symbol
    currency = get_currency_symbol(symbol)
    
    # Try to get company info for better details
    try:
        stock_info = stock.info
        company_name = stock_info.get('longName', symbol)
        currency_from_info = stock_info.get('currency', 'USD')
        
        # Map currency codes to symbols
        currency_symbols = {
            'USD': '$', 'INR': '₹', 'GBP': '£', 'EUR': '€',
            'JPY': '¥', 'CNY': '¥', 'HKD': 'HK$', 'CAD': 'C$',
            'AUD': 'A$', 'KRW': '₩', 'BRL': 'R$'
        }
        currency = currency_symbols.get(currency_from_info, currency)
    except:
        company_name = symbol
    
    return {
        'symbol': symbol,
        'prediction': float(prediction),
        'current_price': float(df['Close'].iloc[-1]),
        'model': model_type,
        'currency': currency,
        'company_name': company_name
    }