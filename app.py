import streamlit as st
import requests
import json

# Set up the page layout
st.set_page_config(page_title="FraudGuard AI", page_icon="🛡️", layout="centered")

st.title("🛡️ FraudGuard - Real-Time Detection")
st.write("Welcome to the Fraud Analyst Dashboard. Click a button below to simulate a transaction coming through the payment gateway.")

# The URL of your FastAPI server
API_URL = "http://127.0.0.1:8080/predict"

# Sample Data 1: A completely normal, safe transaction
normal_tx = {
  "Time": 100.0, "V1": 1.2, "V2": 0.1, "V3": 0.5, "V4": 1.0, "V5": -0.2,
  "V6": -0.5, "V7": 0.1, "V8": -0.1, "V9": 0.2, "V10": -0.1, "V11": 1.1,
  "V12": 0.8, "V13": 0.5, "V14": 0.1, "V15": 0.8, "V16": 0.5, "V17": -0.5,
  "V18": -0.2, "V19": 0.1, "V20": 0.1, "V21": -0.2, "V22": -0.5, "V23": 0.1,
  "V24": 0.2, "V25": 0.5, "V26": 0.1, "V27": -0.1, "V28": 0.0,
  "Amount": 45.50
}

# Sample Data 2: The massive cyberattack fraud we tested earlier
fraud_tx = {
  "Time": 85285.0, "V1": -20.53, "V2": 15.24, "V3": -25.81, "V4": 12.58, "V5": -18.23,
  "V6": -5.55, "V7": -20.45, "V8": 15.01, "V9": -10.84, "V10": -20.88, "V11": 10.43,
  "V12": -15.82, "V13": 0.55, "V14": -18.88, "V15": -0.56, "V16": -12.44, "V17": -20.66,
  "V18": -8.55, "V19": 2.22, "V20": 1.55, "V21": 2.05, "V22": -0.55, "V23": -1.05,
  "V24": 0.22, "V25": 1.05, "V26": 0.55, "V27": 2.05, "V28": 1.05,
  "Amount": 999.99
}

# --- UI BUTTONS ---
col1, col2 = st.columns(2)

with col1:
    if st.button("💳 Simulate Normal Purchase ($45.50)", use_container_width=True):
        st.info("Sending transaction to API...")
        # Send data to the Waiter (API)
        response = requests.post(API_URL, json=normal_tx)
        result = response.json()
        
        # Display the result
        if result["prediction"] == "NORMAL":
            st.success(f"✅ APPROVED: {result['message']}")
        else:
            st.error(f"🚨 BLOCKED: {result['message']}")

with col2:
    if st.button("🏴‍☠️ Simulate Cyberattack ($999.99)", use_container_width=True):
        st.warning("Sending transaction to API...")
        # Send data to the Waiter (API)
        response = requests.post(API_URL, json=fraud_tx)
        result = response.json()
        
        # Display the result
        if result["prediction"] == "FRAUD":
            st.error(f"🚨 ALERT! FRAUD DETECTED: {result['message']}")
        else:
            st.success(f"✅ APPROVED: {result['message']}")

st.markdown("---")
st.write("### Behind the scenes (API Response):")
st.write("When you click a button, the Dashboard receives this exact data back from the FastAPI server:")
# We will show the raw JSON response here when a button is clicked