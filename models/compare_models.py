import pandas as pd 

results = [
    {"Nodel": "Linear Regression", "MAE": 2.5, "RMSE": 3.1},
    {"Model": "Random Forest", "MAE": 1.8, "RMSE": 2.4},
    {"Model": "XGBoost", "MAE": 1.6, "RMSE": 2.1}
    {"Model": "LSTM", "MAE": 1.4, "RMSE": 1.9}
]

best_model = min(results, key=lambda x: x["RMSE"])
print(f"Best Model: {best_model['Model']} with RMSE: {best_model['RMSE']}")

results_df = pd.DataFrame(results)
print(results_df)

results_df.to_csv("data/model_comparison.csv", index=False)