# Model runner utilities
import pandas as pd
from models.xgb_model import run_xgb_model
from risk.volatility import calculate_volatility
from risk.confidence import full_risk_assessment

def run_prediction(symbol):
    df = pd.read_csv(f"data/{symbol}.csv")
    prediction, rmse = run_xgb_model(df)
    volatility = calculate_volatility(df["Close"].values)
    report = full_risk_assessment(
        predicted_price=prediction,
        volatility=volatility,
        rmse=rmse
    )

    return report