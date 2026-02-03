import yfinance as yf
import pandas as pd
import os

# Create directories if they don't exist
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

# Get stock symbol from user
symbol = input("Enter stock symbol: ")

# Download stock data
data = yf.download(symbol, start='2020-01-01', end='2026-02-03')

# Save raw data
data.to_csv('data/raw/raw_data.csv')

# Reset index to make Date a column
data.reset_index(inplace=True)

# Select and rename columns
processed_data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()

# Save processed data WITHOUT the ticker symbol rows
processed_data.to_csv('data/processed/data.csv', index=False)

print(f"Data for {symbol} downloaded and saved successfully!")
print(f"Date range: {processed_data['Date'].min()} to {processed_data['Date'].max()}")
print(f"Total records: {len(processed_data)}")