from sklearn.ensemble import IsolationForest
import numpy as np


import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from email_utils import send_email_alert

# Email config from environment variables for security
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER', 'your_email@gmail.com')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', 'your_app_password')
ALERT_RECIPIENTS = os.environ.get('ALERT_RECIPIENTS', 'recipient@example.com').split(',')

def detect_cost_anomalies(cost_df):
    """Use ML to find cost spikes that deviate from normal."""
    X = cost_df[['cost']].values
    # contamination=0.05 means we expect ~5% of days to be anomalies
    model = IsolationForest(contamination=0.05, random_state=42)
    labels = model.fit_predict(X)
    # IsolationForest returns -1 for anomalies, 1 for normal
    cost_df = cost_df.copy()
    cost_df['is_anomaly'] = labels == -1
    anomalies = cost_df[cost_df['is_anomaly'] == True]
    # Send email alert if anomalies detected
    if not anomalies.empty:
        subject = 'Cloud Cost Anomaly Detected'
        body = f"Anomalies detected in cloud cost data:\n{anomalies.to_string()}"
        send_email_alert(subject, body, ALERT_RECIPIENTS, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
    return anomalies


if __name__ == "__main__":
    import pandas as pd
    np.random.seed(42)
    # Generate 30 days of normal cost data
    costs = np.random.normal(loc=100, scale=10, size=30)
    # Inject anomalies
    costs[5] = 200
    costs[15] = 250
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    cost_df = pd.DataFrame({'date': dates, 'cost': costs})
    anomalies = detect_cost_anomalies(cost_df)
    print("Anomalies detected:")
    print(anomalies)
