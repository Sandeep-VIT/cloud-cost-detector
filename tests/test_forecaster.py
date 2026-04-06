import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data_collector.mock_data import generate_mock_cost_data
from forecaster.cost_predictor import forecast_costs

def test_forecast_runs():
    df = generate_mock_cost_data(days=60)
    forecast = forecast_costs(df)
    assert len(forecast) > 0