# Sentiment Analyzer for News Articles
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment():
    df = pd.read_csv("data/news_data.csv")  # Load your news data CSV file
    sia = SentimentIntensityAnalyzer()

    sentiments = []
    for text in df["headline"]:
        score = sia.polarity_scores(text)["compound"]
        sentiments.append(score)

    df["sentiment"] = sentiments
    df.to_csv("data/news_sentiment.csv", index=False)  # Save the results to a new CSV file
    return df

if __name__ == "__main__":
    analyze_sentiment()