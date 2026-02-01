import pandas as pd

# Load price data
price_data = pd.read_csv('data/processed/data.csv')
price_data["Date"] =  price_data["Date"].str[:10]

# Load sentiment data
sentiment_data = pd.read_csv('data/news_sentiment.csv')
sentiment_data["Date"] = sentiment_data["Date"].str[:10]

# Average sentiment per day
daily_sentiment = sentiment_data.groupby("date")["sentiment"].mean().reset_index()

# Merge datasets
merged_data = price_data.merge(
    daily_sentiment,
    left_on="Date",
    right_on="date",
    how="left"
)

merged_data["sentiment"].fillna(0, inplace=True)
merged_data.to_csv('data/processed/merged_data.csv', index=False)

print("Merged dataset successfully")