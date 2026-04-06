import os
from email_utils import send_email_alert
from dotenv import load_dotenv

load_dotenv()

subject = "Test Email from Cloud Cost Detector"
body = "This is a test email to verify your SMTP and app password setup."
to_emails = os.environ.get('ALERT_RECIPIENTS', 'rsandeepkumar.028@gmail.com').split(',')
smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
smtp_port = int(os.environ.get('SMTP_PORT', 587))
smtp_user = os.environ.get('SMTP_USER', 'rsandeepkumar.028@gmail.com')
smtp_password = os.environ.get('SMTP_PASSWORD', '')

send_email_alert(subject, body, to_emails, smtp_server, smtp_port, smtp_user, smtp_password)
print("Test email sent (if credentials are correct). Check your inbox and spam folder.")
