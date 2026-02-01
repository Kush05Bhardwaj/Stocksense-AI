# Volatility Calculation for Risk Assessment
import numpy as np

def calculatee_volatility(close_prices, window=30):
    """
    Calculate the rolling volatility of stock prices.

    Parameters:
    close_prices (array-like): Array of closing prices.
    window (int): The rolling window size for volatility calculation.

    Returns:
    np.ndarray: Array of rolling volatility values.
    """
    if len(close_prices) < window:
        raise ValueError("Length of close_prices must be greater than the window size.")
    
    recent_prices = close_prices[-window:]
    log_returns = np.diff(np.log(recent_prices))
    rolling_volatility = np.std(log_returns) * np.sqrt(window)
    return rolling_volatility