import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data_collector.mock_data import generate_mock_cost_data
from detector.anomaly_detector import detect_cost_anomalies
from detector.rules_engine import check_idle_compute
import pandas as pd

def test_anomaly_detection_finds_spikes():
    df = generate_mock_cost_data(days=90)
    anomalies = detect_cost_anomalies(df)
    assert len(anomalies) >= 1

def test_idle_compute_detected():
    cpu_df = pd.DataFrame({'Timestamp': range(24), 'Average': [2.0]*24})
    result = check_idle_compute(cpu_df, threshold=5.0)
    assert result is not None
    assert result['leak_type'] == 'IDLE_COMPUTE'