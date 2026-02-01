# News Scraper for Sentiment Analysis
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('NEWS_API_KEY')

def fetch_news(query, from_date, to_date, page_size=100):
    url = ('https://newsapi.org/v2/everything?'
           f'q={query}&'
           f'from={from_date}&'
           f'to={to_date}&'
           f'pageSize={page_size}&'
           'sortBy=relevance&'
           f'apiKey={API_KEY}')
    
    response = requests.get(url)
    articles = response.json().get('articles', [])
    
    news_data = []
    for article in articles:
        news_data.append({
            'title': article['title'],
            'description': article['description'],
            'content': article['content'],
            'publishedAt': article['publishedAt'],
            'source': article['source']['name']
        })
    
    df = pd.DataFrame(news_data)
    df.to_csv(f'data/news_{query}.csv', index=False)
    return df

if __name__ == "__main__":
    query = input("Enter the topic/company to search news for: ")
    from_date = input("Enter the start date (YYYY-MM-DD): ")
    to_date = input("Enter the end date (YYYY-MM-DD): ")
    fetch_news(query, from_date, to_date)