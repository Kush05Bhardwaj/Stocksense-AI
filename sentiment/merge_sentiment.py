import pandas as pd
import matplotlib.pyplot as plt

# Load price data
price_data = pd.read_csv('data/processed/data.csv')
price_data['Date'] = pd.to_datetime(price_data['Date']).dt.date

# Load sentiment data
sentiment_data = pd.read_csv('data/news_sentiment.csv')

# Convert publishedAt to date
sentiment_data['Date'] = pd.to_datetime(sentiment_data['publishedAt']).dt.date

# Average sentiment per day
daily_sentiment = sentiment_data.groupby('Date')['sentiment'].mean().reset_index()

print(f"Price data: {len(price_data)} rows")
print(f"Sentiment data: {len(daily_sentiment)} days")

# Merge datasets
merged_data = price_data.merge(
    daily_sentiment,
    on='Date',
    how='left'
)

# Fill missing sentiment values with 0 (neutral)
merged_data['sentiment'].fillna(0, inplace=True)

# Save merged data
merged_data.to_csv('data/processed/data_with_sentiment.csv', index=False)

print(f"Merged dataset saved: {len(merged_data)} rows")
print(f"Days with sentiment data: {(merged_data['sentiment'] != 0).sum()}")

# Visualization
plt.figure(figsize=(14, 6))

# Plot sentiment on secondary axis
ax1 = plt.subplot(111)
ax2 = ax1.twinx()

ax1.plot(merged_data['Date'], merged_data['Close'], color='blue', label='Closing Price', linewidth=2)
ax2.plot(merged_data['Date'], merged_data['sentiment'], color='orange', label='Daily Sentiment', alpha=0.7)

ax1.set_xlabel('Date')
ax1.set_ylabel('Closing Price ($)', color='blue')
ax2.set_ylabel('Sentiment Score', color='orange')
ax1.set_title('Stock Closing Price and Daily Sentiment Over Time')
ax1.tick_params(axis='y', labelcolor='blue')
ax2.tick_params(axis='y', labelcolor='orange')

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data/visualizations/sentiment_vs_price.png', dpi=300)
plt.show()

print("Visualization saved to data/visualizations/sentiment_vs_price.png")