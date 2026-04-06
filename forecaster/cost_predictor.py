import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_costs(df, days=7):
    # Use dataframe index as time
    df = df.reset_index()
    df['t'] = np.arange(len(df))

    X = df[['t']]
    y = df['cost']

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(df), len(df) + days).reshape(-1, 1)
    predictions = model.predict(future_t)

    result = []
    for i, pred in enumerate(predictions):
        result.append({
            "day": i + 1,
            "predicted_cost": round(float(pred), 2)
        })

    return result