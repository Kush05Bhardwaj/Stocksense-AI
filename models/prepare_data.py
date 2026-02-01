import pandas as pd
import numpy as np

def create_features(df, window=50):
    X, y = [], []
    for i in range(window, len(df)):
        X.append(df['Close'].values[i-window:i])
        y.append(df['Close'].values[i])
    return np.array(X), np.array(y)

def create_feature_with_sentiment(df, window=5):
    X, y = [], []
    for i in range(window, len(df)):
        prices = df['Close'].values[i-window:i]
        sentiment = df["Sentiment"].values[i-window:i]
        features = np.concatenate([prices, sentiment])
        X.append(features)
        y.append(df['Close'].values[i])
    return np.array(X), np.array(y)
