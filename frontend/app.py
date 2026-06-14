import streamlit as st
import requests

st.set_page_config(page_title="FraudGuard AI", page_icon="🛡️", layout="centered")

st.title("🛡️ FraudGuard - Real-Time AI")
st.write("Detect credit card fraud using Machine Learning & FastAPI.")

API_URL = "https://fraudguard-project.onrender.com/predict"

# TẠO 2 TABS SIÊU XỊN
tab1, tab2 = st.tabs(["⚡ Quick Test (Real Data)", "🕵️‍♂️ Manual Entry (Playground)"])

# --- TAB 1: DỮ LIỆU THẬT ---
with tab1:
    st.write("Test the AI using real transaction records from the dataset.")
    col1, col2 = st.columns(2)
    
    # Dữ liệu mẫu lừa đảo thật (Tất cả các V đều bất thường)
    fraud_tx = {
      "Time": 85285.0, "V1": -20.53, "V2": 15.24, "V3": -25.81, "V4": 12.58, "V5": -18.23,
      "V6": -5.55, "V7": -20.45, "V8": 15.01, "V9": -10.84, "V10": -20.88, "V11": 10.43,
      "V12": -15.82, "V13": 0.55, "V14": -18.88, "V15": -0.56, "V16": -12.44, "V17": -20.66,
      "V18": -8.55, "V19": 2.22, "V20": 1.55, "V21": 2.05, "V22": -0.55, "V23": -1.05,
      "V24": 0.22, "V25": 1.05, "V26": 0.55, "V27": 2.05, "V28": 1.05, "Amount": 999.99
    }
    
    normal_tx = {"Time": 100.0, "V1": 1.2, "V2": 0.1, "V3": 0.5, "V4": 1.0, "V5": -0.2, "V6": -0.5, "V7": 0.1, "V8": -0.1, "V9": 0.2, "V10": -0.1, "V11": 1.1, "V12": 0.8, "V13": 0.5, "V14": 0.1, "V15": 0.8, "V16": 0.5, "V17": -0.5, "V18": -0.2, "V19": 0.1, "V20": 0.1, "V21": -0.2, "V22": -0.5, "V23": 0.1, "V24": 0.2, "V25": 0.5, "V26": 0.1, "V27": -0.1, "V28": 0.0, "Amount": 45.50}

    with col1:
        if st.button("💳 Normal Purchase ($45.50)", use_container_width=True):
            with st.spinner("Analyzing..."):
                res = requests.post(API_URL, json=normal_tx).json()
                st.success(f"✅ **APPROVED:** {res['message']}")
    with col2:
        if st.button("🏴‍☠️ Known Cyberattack ($999.99)", use_container_width=True):
            with st.spinner("Analyzing..."):
                res = requests.post(API_URL, json=fraud_tx).json()
                st.error(f"🚨 **FRAUD BLOCKED:** {res['message']}")

# --- TAB 2: NHẬP TAY NGHỊCH NGỢM ---
with tab2:
    st.write("Try to 'hack' the AI by inventing your own transaction data.")
    with st.form("manual_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount ($)", value=150.0)
        with col2:
            time = st.number_input("Time", value=3600.0)

        with st.expander("⚙️ Advanced AI Features"):
            v14 = st.slider("V14", -20.0, 20.0, 0.5)
            v4 = st.slider("V4", -10.0, 10.0, 1.0)
            v12 = st.slider("V12", -20.0, 20.0, 0.5)

        submit = st.form_submit_button("🔍 Check Transaction", use_container_width=True)

    if submit:
        custom_tx = {
            "Time": time, "V1": 0.0, "V2": 0.0, "V3": 0.0, "V4": v4, "V5": 0.0,
            "V6": 0.0, "V7": 0.0, "V8": 0.0, "V9": 0.0, "V10": 0.0, "V11": 0.0,
            "V12": v12, "V13": 0.0, "V14": v14, "V15": 0.0, "V16": 0.0, "V17": 0.0,
            "V18": 0.0, "V19": 0.0, "V20": 0.0, "V21": 0.0, "V22": 0.0, "V23": 0.0,
            "V24": 0.0, "V25": 0.0, "V26": 0.0, "V27": 0.0, "V28": 0.0, "Amount": amount
        }
        with st.spinner("Analyzing..."):
            res = requests.post(API_URL, json=custom_tx).json()
            if res["prediction"] == "FRAUD":
                st.error(f"🚨 **FRAUD BLOCKED:** {res['message']}")
            else:
                st.success(f"✅ **APPROVED:** {res['message']}")