import streamlit as st
import json
import requests
from kafka import KafkaConsumer

# Set up the UI
st.set_page_config(page_title="Live Fraud Feed", page_icon="🔴", layout="wide")
st.title("🔴 Live Global Transaction Feed")
st.write("Real-time monitoring powered by Kafka, FastAPI, and Docker.")

API_URL = "http://127.0.0.1:8080/predict"

# Create empty boxes in the UI that we will fill with live data
col1, col2 = st.columns(2)
total_tx_box = col1.empty()
fraud_tx_box = col2.empty()

st.subheader("Live Activity Log:")
log_box = st.empty()

# Add a button to start the stream
if st.button("▶️ Start Live Stream"):
    st.success("Connected to Kafka! Waiting for transactions...")
    
    # 1. Connect to Kafka
    consumer = KafkaConsumer(
        'fraud_stream',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    tx_count = 0
    fraud_count = 0
    logs = []
    
    # 2. Continuously read from the stream
    for message in consumer:
        transaction = message.value
        
        try:
            # Send to your Docker AI API
            response = requests.post(API_URL, json=transaction)
            result = response.json()
            
            tx_count += 1
            
            # Update counts and logs based on the AI's prediction
            if result["prediction"] == "FRAUD":
                fraud_count += 1
                logs.insert(0, f"🚨 FRAUD BLOCKED! Amount: ${transaction['Amount']} | Time: {transaction['Time']}")
            else:
                logs.insert(0, f"✅ APPROVED | Amount: ${transaction['Amount']}")
            
            # Keep only the last 15 logs so the screen doesn't get too long
            if len(logs) > 15:
                logs.pop()
                
            # 3. Update the Streamlit UI IN REAL TIME!
            total_tx_box.metric("Total Transactions Scanned", tx_count)
            fraud_tx_box.metric("⚠️ Frauds Blocked", fraud_count)
            
            # Print the logs to the screen
            log_box.code('\n'.join(logs))
            
        except Exception as e:
            st.error(f"Error connecting to AI API: {e}")
            break