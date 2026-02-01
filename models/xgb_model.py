# XGBoost Model for Stock Price Prediction
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error 
from xgboost import XGBRegressor
from prepare_data import create_features, create_features_with_sentiment

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

print(f"XGBoost Model Performance:")
print(f"Mean Squared Error: {mse}")
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Squared Error: {rmse}")


if sentiment_data < -0.3:
    confidence = "Low (High Negative Sentiment)"
elif sentiment_data > 0.3:
    confidence = "High (High Positive Sentiment)"
else:
    confidence = "Medium (Neutral Sentiment)"
    
