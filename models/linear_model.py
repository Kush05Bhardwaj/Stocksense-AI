# Linear Regression Model for Stock Price Prediction
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from prepare_data import create_features
import numpy as np
import pandas as pd

df = pd.read_csv('data/processed/data.csv')
X, y = create_features(df)

split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]  
y_train, y_test = y[:split], y[split:]

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Linear Regression Model Performance:")
print(f"Mean Squared Error: {mse}")
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Squared Error: {rmse}")