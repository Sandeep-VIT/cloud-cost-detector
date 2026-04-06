import subprocess

# Start Flask API
subprocess.Popen(["python", "api/app.py"])

# Start Streamlit Dashboard
subprocess.Popen([
    "streamlit", "run", "dashboard.py",
    "--server.port", "8501",
    "--server.address", "0.0.0.0"
])

# Keep container running
import time
while True:
    time.sleep(60)