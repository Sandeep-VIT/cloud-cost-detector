import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_cost_data(days=90):
    """Generate realistic fake daily cost data with some anomalies."""
    dates = [datetime.today() - timedelta(days=i) for i in range(days)]
    # Normal cost: ~$5/day with small random variation
    costs = np.random.normal(loc=5.0, scale=0.5, size=days)
    # Add a spike on day 30 (simulate unexpected cost)
    costs[30] = costs[30] * 4.0
    df = pd.DataFrame({'date': dates, 'cost': costs})
    df = df.sort_values('date').reset_index(drop=True)
    return df
