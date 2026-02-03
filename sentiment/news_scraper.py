# News Scraper for Sentiment Analysis
import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.getenv('NEWS_API_KEY')

def fetch_news(query, from_date, to_date, page_size=100):
    if not API_KEY:
        print("ERROR: NEWS_API_KEY not found in .env file!")
        print("Please create a .env file and add: NEWS_API_KEY=your_api_key_here")
        return pd.DataFrame()
    
    url = ('https://newsapi.org/v2/everything?'
           f'q={query}&'
           f'from={from_date}&'
           f'to={to_date}&'
           f'pageSize={page_size}&'
           'sortBy=relevance&'
           f'apiKey={API_KEY}')
    
    print(f"Fetching news for '{query}' from {from_date} to {to_date}...")
    
    response = requests.get(url)
    
    # Check response status
    if response.status_code != 200:
        print(f"ERROR: API returned status code {response.status_code}")
        print(f"Response: {response.text}")
        return pd.DataFrame()
    
    data = response.json()
    
    # Check for API errors
    if data.get('status') != 'ok':
        print(f"ERROR: {data.get('message', 'Unknown error')}")
        return pd.DataFrame()
    
    articles = data.get('articles', [])
    print(f"Found {len(articles)} articles")
    
    if len(articles) == 0:
        print("No articles found. Try different dates or search terms.")
        return pd.DataFrame()
    
    news_data = []
    for article in articles:
        news_data.append({
            'title': article.get('title', ''),
            'description': article.get('description', ''),
            'content': article.get('content', ''),
            'publishedAt': article.get('publishedAt', ''),
            'source': article.get('source', {}).get('name', '')
        })
    
    df = pd.DataFrame(news_data)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    filename = f'data/news.csv'
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} articles to {filename}")
    
    return df

if __name__ == "__main__":
    query = input("Enter the topic/company to search news for: ")
    from_date = input("Enter the start date (YYYY-MM-DD): ")
    to_date = input("Enter the end date (YYYY-MM-DD): ")
    fetch_news(query, from_date, to_date)