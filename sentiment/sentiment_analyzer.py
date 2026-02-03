# Sentiment Analyzer for News Articles
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# Download VADER lexicon if not already downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download('vader_lexicon')

def analyze_sentiment(news_file='data/news.csv'):
    """
    Analyze sentiment of news articles
    """
    # Check if file exists
    if not os.path.exists(news_file):
        print(f"ERROR: News file not found at {news_file}")
        print("Please run news_scraper.py first to fetch news articles.")
        return None
    
    df = pd.read_csv(news_file)
    
    print(f"Loaded {len(df)} articles")
    print(f"Columns: {df.columns.tolist()}")
    
    sia = SentimentIntensityAnalyzer()

    sentiments = []
    for idx, row in df.iterrows():
        # Combine title and description for better sentiment analysis
        text = str(row.get('title', '')) + ' ' + str(row.get('description', ''))
        
        # Get sentiment scores
        score = sia.polarity_scores(text)
        sentiments.append({
            'compound': score['compound'],
            'positive': score['pos'],
            'negative': score['neg'],
            'neutral': score['neu']
        })

    # Add sentiment scores to dataframe
    df['sentiment'] = [s['compound'] for s in sentiments]
    df['sentiment_pos'] = [s['positive'] for s in sentiments]
    df['sentiment_neg'] = [s['negative'] for s in sentiments]
    df['sentiment_neu'] = [s['neutral'] for s in sentiments]
    
    # Save results
    output_file = news_file.replace('.csv', '_sentiment.csv')
    df.to_csv(output_file, index=False)
    
    print(f"\nSentiment Analysis Complete!")
    print(f"Saved results to {output_file}")
    print(f"\nSentiment Statistics:")
    print(f"Average Sentiment: {df['sentiment'].mean():.3f}")
    print(f"Positive articles: {len(df[df['sentiment'] > 0.05])}")
    print(f"Negative articles: {len(df[df['sentiment'] < -0.05])}")
    print(f"Neutral articles: {len(df[df['sentiment'].between(-0.05, 0.05)])}")
    
    return df

if __name__ == "__main__":
    analyze_sentiment()