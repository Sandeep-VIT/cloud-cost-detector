import os
from data_collector.mock_data import generate_mock_cost_data
from detector.anomaly_detector import detect_cost_anomalies
from email_utils import send_email_alert
from dotenv import load_dotenv

def main():
    # Load environment variables from .env
    load_dotenv()
    
    print("Gathering cost data and detecting anomalies...")
    # Generate data and find anomalies
    df = generate_mock_cost_data(days=90)
    anomalies = detect_cost_anomalies(df)
    
    if len(anomalies) > 0:
        print(f"Detected {len(anomalies)} anomalies!")
        print(anomalies)
        
        # Format the anomaly details into an email body
        body = "Cloud Cost Detection System has identified the following anomalies in your AWS bill:\n\n"
        for idx, row in anomalies.iterrows():
            date_str = row['date'].strftime('%Y-%m-%d')
            body += f"- Date {date_str}: Cost spiked to ${row['cost']:.2f}\n"
        
        body += "\nPlease investigate these spikes in your cloud resources immediately to prevent budget overruns.\n"
        body += "\nBest,\nYour Cloud Cost Monitor"
        
        # Gather SMTP settings
        subject = f"⚠️ ALERT: {len(anomalies)} Cloud Cost Anomalies Detected!"
        to_emails = os.environ.get('ALERT_RECIPIENTS', 'rsandeepkumar.028@gmail.com').split(',')
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_user = os.environ.get('SMTP_USER', 'rsandeepkumar.028@gmail.com')
        smtp_password = os.environ.get('SMTP_PASSWORD', '') # Make sure to fill in .env!
        
        print("Sending alert email...")
        send_email_alert(
            subject=subject,
            body=body,
            to_emails=to_emails,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password
        )
    else:
        print("No anomalies detected today.")

if __name__ == "__main__":
    main()
