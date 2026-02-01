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

if __name__ == "__main__":
    # Example usage
    sentiment_data = 0.5  # Replace with actual sentiment value
    confidence = calculate_confidence(sentiment_data)
    print(f"Confidence: {confidence}")