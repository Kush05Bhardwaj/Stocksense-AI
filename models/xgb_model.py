# XGBoost Model for Stock Price Prediction with Sentiment Analysis
import pandas as pd
import numpy as np
import sys
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error
import xgboost as xgb

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.prepare_data import create_features

# Try to load data with sentiment, fall back to regular data
try:
    df = pd.read_csv('data/processed/data_with_sentiment.csv')
    has_sentiment = 'sentiment' in df.columns
except FileNotFoundError:
    df = pd.read_csv('data/processed/data.csv')
    has_sentiment = False
    print("Sentiment data not found. Using price data only.")

X, y = create_features(df, window=5)

split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"XGBoost Model Performance:")
print(f"Mean Squared Error: {mse}")
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Squared Error: {rmse}")
if has_sentiment:
    print("(trained with sentiment data)")