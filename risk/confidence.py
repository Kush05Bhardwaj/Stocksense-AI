# Confidence Score Calculation

def calculate_confidence(sentiment_data):
    """
    Calculate confidence level based on sentiment score.
    
    Args:
        sentiment_data (float): Sentiment score (typically between -1 and 1)
    
    Returns:
        str: Confidence level description
    """
    if sentiment_data < -0.3:
        confidence = "Low (High Negative Sentiment)"
    elif sentiment_data > 0.3:
        confidence = "High (High Positive Sentiment)"
    else:
        confidence = "Medium (Neutral Sentiment)"
    
    return confidence

def confidence_interval(predicted_price, rmse):
    """
    Calculate confidence interval for predicted stock price.
    
    Args:
        predicted_price (float): The predicted stock price
        rmse (float): Root Mean Squared Error of the model

    Returns:
        tuple: Lower and upper bounds of the confidence interval
    """
    lower_bound = predicted_price - rmse
    upper_bound = predicted_price + rmse
    return (lower_bound, upper_bound)

def risk_level(volatility):
    """
    Determine risk level based on stock volatility.
    
    Args:
        volatility (float): Volatility measure of the stock
    
    Returns:
        str: Risk level description
    """
    if volatility < 10:
        return "Low Risk"
    elif volatility < 25:
        return "Medium Risk"
    else:
        return "High Risk"

def full_risk_assessment(predicted_price, rmse, volatility, sentiment_data):
    """
    Perform a full risk assessment combining confidence interval, risk level, and sentiment-based confidence.
    
    Args:
        predicted_price (float): The predicted stock price
        rmse (float): Root Mean Squared Error of the model
        volatility (float): Volatility measure of the stock
        sentiment_data (float): Sentiment score (typically between -1 and 1)
    
    Returns:
        dict: Comprehensive risk assessment
    """
    lower_bound, upper_bound = confidence_interval(predicted_price, rmse)
    risk = risk_level(volatility)
    confidence = calculate_confidence(sentiment_data)

    if sentiment_data < -0.3:
        risk += " with Increased Risk due to Negative Sentiment"
    elif sentiment_data > 0.3:
        risk += " with Decreased Risk due to Positive Sentiment"

    return {
        "predicted_price": round(predicted_price, 2),
        "confidence_interval": (lower_bound, upper_bound),
        "confidence_range": (upper_bound, lower_bound),
        "risk_level": risk,
        "sentiment_confidence": confidence
    }

if __name__ == "__main__":
    # Example usage
    predicted_price = 150.0
    rmse = 5.0
    volatility = 20.0
    sentiment_data = 0.4

    assessment = full_risk_assessment(predicted_price, rmse, volatility, sentiment_data)
    print("Full Risk Assessment:")
    for key, value in assessment.items():
        print(f"{key}: {value}")