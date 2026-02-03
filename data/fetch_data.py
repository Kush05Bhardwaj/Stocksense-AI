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

# Save raw data with proper handling
data.to_csv('data/raw/raw_data.csv')

# Reset index to make Date a column
data = data.reset_index()

# Flatten column names if multi-level (remove ticker symbol level)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Ensure column names are strings and clean
data.columns = [str(col).strip() for col in data.columns]

# Select and rename columns - make a clean copy
processed_data = pd.DataFrame({
    'Date': data['Date'],
    'Open': pd.to_numeric(data['Open'], errors='coerce'),
    'High': pd.to_numeric(data['High'], errors='coerce'),
    'Low': pd.to_numeric(data['Low'], errors='coerce'),
    'Close': pd.to_numeric(data['Close'], errors='coerce'),
    'Volume': pd.to_numeric(data['Volume'], errors='coerce')
})

# Drop any rows with NaN values
processed_data = processed_data.dropna()

# Save processed data
processed_data.to_csv('data/processed/data.csv', index=False)

print(f"Data for {symbol} downloaded and saved successfully!")
print(f"Date range: {processed_data['Date'].min()} to {processed_data['Date'].max()}")
print(f"Total records: {len(processed_data)}")