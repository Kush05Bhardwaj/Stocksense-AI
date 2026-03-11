import yfinance as yf
from datetime import datetime
from utils.model_runner import run_all_predictions

def generate_report(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    info = ticker.info

    # --- Company Overview ---
    overview = {
        "name": info.get("longName", symbol),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "description": info.get("longBusinessSummary", "N/A"),
        "website": info.get("website", "N/A"),
        "employees": info.get("fullTimeEmployees", "N/A"),
        "country": info.get("country", "N/A"),
    }

    # --- Financial Health ---
    financial = {
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "eps": info.get("trailingEps"),
        "dividend_yield": info.get("dividendYield"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "price_to_book": info.get("priceToBook"),
        "debt_to_equity": info.get("debtToEquity"),
        "profit_margin": info.get("profitMargins"),
        "revenue_growth": info.get("revenueGrowth"),
        "current_ratio": info.get("currentRatio"),
    }

    # --- News Sentiment via yfinance ---
    from sentiment.sentiment_analyzer import analyze_sentiment
    news = ticker.news[:10]  # latest 10 headlines
    scores = []
    for article in news:
        title = article.get("title", "")
        score = analyze_sentiment(title)   # re-use existing analyzer
        scores.append(score)
    avg_sentiment = sum(scores) / len(scores) if scores else 0
    sentiment_label = "Positive" if avg_sentiment > 0.1 else "Negative" if avg_sentiment < -0.1 else "Neutral"

    # --- ML Predictions ---
    pred_data = run_all_predictions(symbol)
    predictions = pred_data["predictions"]
    current_price = pred_data["current_price"]
    currency = pred_data["currency"]

    # --- Risk Assessment ---
    import yfinance as yf
    import numpy as np
    hist = ticker.history(period="1y")
    prices = hist["Close"].values
    log_returns = np.diff(np.log(prices))
    volatility = float(np.std(log_returns) * np.sqrt(252) * 100)   # annualised %
    risk_level = "Low" if volatility < 20 else "High" if volatility > 40 else "Medium"

    # --- Bull vs Bear ---
    bull_args, bear_args = build_bull_bear(
        info, avg_sentiment, predictions, current_price, volatility
    )

    # --- Recommendation Score (0-100) ---
    rec = compute_recommendation(avg_sentiment, predictions, current_price, volatility, financial)

    report = {
        "symbol": symbol,
        "generated_at": datetime.utcnow().isoformat(),
        "currency": currency,
        "current_price": current_price,
        "company_overview": overview,
        "financial_health": financial,
        "news_sentiment": {
            "score": round(avg_sentiment, 4),
            "label": sentiment_label,
            "total_articles": len(news),
        },
        "predictions": predictions,
        "risk": {
            "annualised_volatility_pct": round(volatility, 2),
            "risk_level": risk_level,
        },
        "bull_arguments": bull_args,
        "bear_arguments": bear_args,
        "recommendation": rec,
    }

    return report