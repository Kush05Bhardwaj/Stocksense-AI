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


if __name__ == "__main__":
    # Example usage
    sentiment_data = 0.5  # Replace with actual sentiment value
    confidence = calculate_confidence(sentiment_data)
    print(f"Confidence: {confidence}")