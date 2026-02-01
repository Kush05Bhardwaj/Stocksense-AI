# XGBoost Model for Stock Price Prediction
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error 
from xgboost import XGBRegressor
from prepare_data import create_features, create_features_with_sentiment
from risk.volatility import calculate_volatility
from risk.confidence import full_risk_assessment


df = pd.read_csv('data/processed/price_with_sentiment.csv')
prices = df['Close'].values

X, y = create_features_with_sentiment(df, window=5)

split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)

vol = calculate_volatility(df['Close'].values)
report = full_risk_assessment(
    predicted_price=preds[-1],
    rmse=rmse,
    volatility=vol,
    sentiment_data=df['Sentiment'].values
)

print(f"XGBoost Model Performance:")
print(f"Mean Squared Error: {mse}")
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Squared Error: {rmse}")
    
