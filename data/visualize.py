import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the cleaned CSV
df = pd.read_csv('data/processed/data.csv', parse_dates=['Date'], index_col='Date')

print("Data loaded successfully!")
print(f"Date range: {df.index.min()} to {df.index.max()}")
print(f"Total records: {len(df)}")

# Calculate moving averages
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

# Create visualization
plt.figure(figsize=(12,6))
plt.plot(df.index, df['Close'], label='Close Price', linewidth=1.5)
plt.plot(df.index, df['MA20'], label='20-Day MA', alpha=0.7)
plt.plot(df.index, df['MA50'], label='50-Day MA', alpha=0.7)
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.title('Stock Price with Moving Averages')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Create visualizations directory if it doesn't exist
os.makedirs('data/visualizations', exist_ok=True)

plt.savefig('data/visualizations/stock_price.png', dpi=300)
plt.show()
print("\nVisualization saved to data/visualizations/stock_price.png")