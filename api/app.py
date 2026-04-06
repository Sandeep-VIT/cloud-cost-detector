import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from data_collector.mock_data import generate_mock_cost_data
from detector.anomaly_detector import detect_cost_anomalies
from forecaster.cost_predictor import forecast_costs
from email_utils import send_email_alert
from flask import request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/detect")
def detect():
    df = generate_mock_cost_data(days=90)
    anomalies = detect_cost_anomalies(df)
    return {"anomalies": anomalies.to_dict(orient="records"), "count": len(anomalies)}

@app.route("/forecast")
def forecast():
    days = int(request.args.get("days", 7))
    df = generate_mock_cost_data(days=60)
    result = forecast_costs(df, days=days)
    return {"forecast": result}

@app.route("/live_data")
def live_data():
    import numpy as np
    from datetime import datetime
    cost = max(0, np.random.normal(loc=5.0, scale=0.5))
    is_anomaly = False
    if np.random.rand() < 0.05:
        cost = cost * 4.0
        is_anomaly = True
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {"date": date_str, "cost": round(cost, 2), "is_anomaly": is_anomaly}

@app.route("/send_alert", methods=['POST'])
def send_alert():
    data = request.json
    cost = data.get('cost')
    date = data.get('date')
    body = f"Cloud Cost System simulated a LIVE anomaly!\n\nTime: {date}\nSpike Cost: ${cost:.2f}\n\nPlease investigate your infrastructure immediately.\n"
    subject = "⚠️ LIVE ALERT: Sudden Cloud Cost Anomaly Detected!"
    to_emails = os.environ.get('ALERT_RECIPIENTS', 'rsandeepkumar.028@gmail.com').split(',')
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    
    send_email_alert(subject, body, to_emails, smtp_server, smtp_port, smtp_user, smtp_password)
    return {"status": "alert sent"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)