import sys
import os
import numpy as np
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import yfinance as yf
from utils.model_runner import run_all_predictions

# ---------------------------------------------------------------------------
# VADER sentiment scorer — operates on raw text (not a CSV file)
# ---------------------------------------------------------------------------
try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)
    _sia = SentimentIntensityAnalyzer()

    def _score_text(text: str) -> float:
        return _sia.polarity_scores(str(text))['compound']
except Exception:
    def _score_text(text: str) -> float:  # graceful fallback
        return 0.0


# ---------------------------------------------------------------------------
# Bull / Bear argument builder
# ---------------------------------------------------------------------------
def build_bull_bear(info: dict, avg_sentiment: float, predictions: list,
                    current_price: float, volatility: float):
    bull, bear = [], []

    # Prediction consensus
    pos = [p for p in predictions if p['change'] > 0]
    neg = [p for p in predictions if p['change'] < 0]
    if pos:
        avg_gain = sum(p['change'] for p in pos) / len(pos)
        bull.append(
            f"{len(pos)} of {len(predictions)} models predict an average gain of {avg_gain:.1f}%."
        )
    if neg:
        avg_loss = abs(sum(p['change'] for p in neg) / len(neg))
        bear.append(
            f"{len(neg)} of {len(predictions)} models predict an average decline of {avg_loss:.1f}%."
        )

    # News sentiment
    if avg_sentiment > 0.1:
        bull.append(
            f"Positive news sentiment (score: {avg_sentiment:+.2f}) indicates a favourable market perception."
        )
    elif avg_sentiment < -0.1:
        bear.append(
            f"Negative news sentiment (score: {avg_sentiment:+.2f}) suggests an adverse market outlook."
        )

    # 52-week range
    high_52 = info.get('fiftyTwoWeekHigh')
    low_52  = info.get('fiftyTwoWeekLow')
    if high_52 and low_52 and current_price:
        pct_from_high = ((high_52 - current_price) / high_52) * 100
        pct_from_low  = ((current_price - low_52) / low_52) * 100
        if pct_from_high > 15:
            bull.append(
                f"Price is {pct_from_high:.1f}% below its 52-week high, suggesting meaningful upside room."
            )
        if pct_from_high < 5:
            bear.append(
                f"Price is within {pct_from_high:.1f}% of its 52-week high, limiting near-term upside."
            )
        if pct_from_low < 10:
            bear.append(
                f"Price is only {pct_from_low:.1f}% off its 52-week low, indicating recent weakness."
            )

    # Valuation (P/E)
    pe = info.get('trailingPE')
    if pe and pe > 0:
        if pe < 15:
            bull.append(f"Low trailing P/E of {pe:.1f}x suggests the stock may be undervalued.")
        elif pe > 40:
            bear.append(f"Elevated trailing P/E of {pe:.1f}x suggests the stock may be overvalued.")

    # Debt-to-equity
    de = info.get('debtToEquity')
    if de is not None:
        if de > 150:
            bear.append(f"High debt-to-equity ratio of {de:.0f}% raises financial leverage concerns.")
        elif de < 50:
            bull.append(f"Low debt-to-equity ratio of {de:.0f}% reflects solid balance-sheet health.")

    # Revenue growth
    rv = info.get('revenueGrowth')
    if rv is not None:
        if rv > 0.10:
            bull.append(f"Strong revenue growth of {rv * 100:.1f}% demonstrates robust business expansion.")
        elif rv < 0:
            bear.append(f"Declining revenue ({rv * 100:.1f}%) signals potential top-line headwinds.")

    # Profit margin
    margin = info.get('profitMargins')
    if margin is not None:
        if margin > 0.15:
            bull.append(f"Healthy profit margin of {margin * 100:.1f}% indicates strong operational efficiency.")
        elif margin < 0:
            bear.append(f"Negative profit margin ({margin * 100:.1f}%) points to ongoing profitability challenges.")

    # Volatility
    if volatility > 40:
        bear.append(f"High annualised volatility of {volatility:.1f}% indicates elevated price risk.")
    elif volatility < 20:
        bull.append(f"Low annualised volatility of {volatility:.1f}% suggests a stable, lower-risk profile.")

    return bull, bear


# ---------------------------------------------------------------------------
# Recommendation scorer  (0–100 → BUY / HOLD / SELL)
# ---------------------------------------------------------------------------
def compute_recommendation(avg_sentiment: float, predictions: list,
                            current_price: float, volatility: float,
                            financial: dict) -> dict:
    score = 50.0

    # Prediction signal (±20 pts)
    if predictions:
        avg_change = sum(p['change'] for p in predictions) / len(predictions)
        score += min(max(avg_change * 2, -20), 20)

    # Sentiment (±15 pts)
    score += avg_sentiment * 15

    # Volatility penalty (up to -10 pts)
    if volatility > 40:
        score -= 10
    elif volatility > 25:
        score -= 5

    # Valuation via P/E (±10 pts)
    pe = financial.get('pe_ratio')
    if pe and pe > 0:
        if pe < 15:
            score += 10
        elif pe < 25:
            score += 5
        elif pe > 40:
            score -= 10

    # Leverage (±5 pts)
    de = financial.get('debt_to_equity')
    if de is not None:
        score += 5 if de < 50 else (-5 if de > 150 else 0)

    # Revenue growth (±5 pts)
    rv = financial.get('revenue_growth')
    if rv is not None:
        score += 5 if rv > 0.10 else (-5 if rv < 0 else 0)

    score = round(min(max(score, 0), 100))
    signal = 'BUY' if score >= 65 else 'SELL' if score <= 40 else 'HOLD'

    if predictions:
        avg_change = sum(p['change'] for p in predictions) / len(predictions)
        pred_text = f"ML models project an average price change of {avg_change:+.1f}%"
    else:
        pred_text = "Insufficient prediction data"

    sent_word = ('positive' if avg_sentiment > 0.1
                 else 'negative' if avg_sentiment < -0.1
                 else 'neutral')
    rationale = (
        f"{pred_text}. News sentiment is {sent_word} (score: {avg_sentiment:+.2f}), "
        f"and annualised volatility stands at {volatility:.1f}%. "
        f"Overall confidence score: {score}/100."
    )

    return {'score': score, 'signal': signal, 'rationale': rationale}


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def generate_report(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    info = ticker.info

    # --- Company Overview ---
    overview = {
        'name':        info.get('longName', symbol),
        'sector':      info.get('sector', 'N/A'),
        'industry':    info.get('industry', 'N/A'),
        'description': info.get('longBusinessSummary', 'N/A'),
        'website':     info.get('website', 'N/A'),
        'employees':   info.get('fullTimeEmployees', 'N/A'),
        'country':     info.get('country', 'N/A'),
    }

    # --- Financial Health ---
    financial = {
        'market_cap':     info.get('marketCap'),
        'pe_ratio':       info.get('trailingPE'),
        'forward_pe':     info.get('forwardPE'),
        'eps':            info.get('trailingEps'),
        'dividend_yield': info.get('dividendYield'),
        '52_week_high':   info.get('fiftyTwoWeekHigh'),
        '52_week_low':    info.get('fiftyTwoWeekLow'),
        'price_to_book':  info.get('priceToBook'),
        'debt_to_equity': info.get('debtToEquity'),
        'profit_margin':  info.get('profitMargins'),
        'revenue_growth': info.get('revenueGrowth'),
        'current_ratio':  info.get('currentRatio'),
    }

    # --- News Sentiment (score each headline live with VADER) ---
    news = ticker.news[:10]
    scores = [_score_text(a.get('title', '')) for a in news]
    avg_sentiment = sum(scores) / len(scores) if scores else 0.0
    sentiment_label = (
        'Positive' if avg_sentiment > 0.1
        else 'Negative' if avg_sentiment < -0.1
        else 'Neutral'
    )

    # --- ML Predictions ---
    pred_data     = run_all_predictions(symbol)
    predictions   = pred_data['predictions']
    current_price = pred_data['current_price']
    currency      = pred_data['currency']

    # --- Risk (annualised volatility from 1-year daily log-returns) ---
    hist        = ticker.history(period='1y')
    prices      = hist['Close'].values
    log_returns = np.diff(np.log(prices))
    volatility  = float(np.std(log_returns) * np.sqrt(252) * 100)
    risk_level  = 'Low' if volatility < 20 else 'High' if volatility > 40 else 'Medium'

    # --- Bull vs Bear ---
    bull_args, bear_args = build_bull_bear(
        info, avg_sentiment, predictions, current_price, volatility
    )

    # --- Recommendation ---
    rec = compute_recommendation(
        avg_sentiment, predictions, current_price, volatility, financial
    )

    return {
        'symbol':           symbol,
        'generated_at':     datetime.utcnow().isoformat(),
        'currency':         currency,
        'current_price':    current_price,
        'company_overview': overview,
        'financial_health': financial,
        'news_sentiment': {
            'score':          round(avg_sentiment, 4),
            'label':          sentiment_label,
            'total_articles': len(news),
        },
        'predictions':     predictions,
        'risk': {
            'annualised_volatility_pct': round(volatility, 2),
            'risk_level':               risk_level,
        },
        'bull_arguments':  bull_args,
        'bear_arguments':  bear_args,
        'recommendation':  rec,
    }