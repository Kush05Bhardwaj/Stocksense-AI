import pandas as pd
import numpy as np

def create_features(df, window=50):
    X, y = [], []
    for i in range(window, len(df)):
        X.append(df['Close'].values[i-window:i])
        y.append(df['Close'].values[i])
    return np.array(X), np.array(y)