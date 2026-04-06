import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Cloud Cost Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- Premium Aesthetics (Glassmorphism & Modern styling) ---
st.markdown("""
<style>
    /* Main body background overlay */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f, #151520);
        color: white;
    }
    
    /* Center aligning titles */
    h1, h2, h3 {
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism elements */
    .st-emotion-cache-1wivap2 {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("☁️ Premium Cloud Cost Monitor")

# Sidebar Toggle
mode = st.sidebar.radio("Dashboard Mode", ["Demo Data (Historical)", "Live Data (Streaming)"])
st.sidebar.markdown("---")
# Health Status via sidebar
try:
    health = requests.get(f"{API_URL}/health").json()
    st.sidebar.success(f"Backend Status: {health['status']}")
except Exception:
    st.sidebar.error("Backend Status: Offline")


if mode == "Demo Data (Historical)":
    st.header("Demo Data Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cost Anomalies Detection")
        try:
            detect = requests.get(f"{API_URL}/detect").json()
            if detect["count"] > 0:
                st.error(f"⚠️ {detect['count']} historical anomalies detected!")
                df_anom = pd.DataFrame(detect["anomalies"])
                st.dataframe(df_anom, use_container_width=True)
            else:
                st.success("No anomalies detected in the past 90 days.")
        except Exception:
            st.error("Failed to fetch detection data.")

    with col2:
        st.subheader("Monthly Cost Predictor (30 Days)")
        try:
            forecast = requests.get(f"{API_URL}/forecast?days=30").json()
            df_forecast = pd.DataFrame(forecast["forecast"])
            
            # Simple chart
            fig, ax = plt.subplots(figsize=(6,4))
            ax.plot(df_forecast["day"], df_forecast["predicted_cost"], color="#00ffcc", linewidth=2)
            ax.set_facecolor('#1e1e2f')
            fig.patch.set_facecolor('#1e1e2f')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.set_xlabel("Day", color="white")
            ax.set_ylabel("Predicted Cost ($)", color="white")
            st.pyplot(fig)
            
            total_predicted = df_forecast['predicted_cost'].sum()
            st.info(f"**Estimated Total Cost for Next 30 Days:** ${total_predicted:.2f}")
        except Exception:
            st.error("Failed to fetch forecast.")
            
    st.markdown("---")
    st.subheader("Old Data (Historical Log)")
    tab1, tab2 = st.tabs(["Anomaly History", "Forecast Detailed Breakdown"])
    with tab1:
        if 'detect' in locals() and detect.get("count", 0) > 0:
            st.dataframe(df_anom, use_container_width=True)
        else:
            st.write("No historical anomalies to display.")
    
    with tab2:
        if 'df_forecast' in locals():
            st.dataframe(df_forecast, use_container_width=True)


elif mode == "Live Data (Streaming)":
    st.header("Live Cost Data Stream")
    
    if "live_history" not in st.session_state:
        st.session_state.live_history = []
        
    placeholder = st.empty()
    alert_placeholder = st.empty()
    
    @st.fragment(run_every="2s")
    def fetch_live_data():
        try:
            res = requests.get(f"{API_URL}/live_data").json()
            history = st.session_state.live_history
            history.append(res)
            # Keep max 50 items
            if len(history) > 50:
                history.pop(0)
            
            df = pd.DataFrame(history)
            
            with placeholder.container():
                st.subheader(f"Current Metric: ${res['cost']:.2f}")
                st.line_chart(df.set_index('date')['cost'], height=300)
                
            if res.get('is_anomaly'):
                with alert_placeholder.container():
                    st.error(f"🚨 BOOM! Sudden Anomaly Detected! Cost spiked to ${res['cost']:.2f} at {res['date']}! Alert Email is being dispatched!")
                # Dispatch Email
                requests.post(f"{API_URL}/send_alert", json={"cost": res['cost'], "date": res['date']})
            else:
                alert_placeholder.empty()
                
        except Exception as e:
            placeholder.error(f"Live backend unreachable. Error: {e}")

    fetch_live_data()
    
    st.markdown("---")
    st.subheader("Monthly Cost Predictor")
    try:
        forecast = requests.get(f"{API_URL}/forecast?days=30").json()
        total_predicted = sum([i['predicted_cost'] for i in forecast['forecast']])
        st.metric("30-Day Estimated Forecast", f"${total_predicted:.2f}")
    except:
        pass