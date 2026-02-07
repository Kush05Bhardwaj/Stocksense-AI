# Sentiment analysis routes
from flask import Blueprint, jsonify
import pandas as pd

sentiment_bp = Blueprint('sentiment', __name__)

@sentiment_bp.route('/sentiment/<symbol>', methods=['GET'])
def get_sentiment(symbol):
    try:
        df = pd.read_csv(f'data/news_{symbol}_sentiment.csv')
        avg_sentiment = df['sentiment'].mean()
        
        return jsonify({
            'symbol': symbol,
            'average_sentiment': float(avg_sentiment),
            'total_articles': len(df)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404