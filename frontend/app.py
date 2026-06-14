import streamlit as st
import requests

st.set_page_config(page_title="FraudGuard AI", page_icon="🛡️", layout="centered")

st.title("🛡️ FraudGuard - AI Detective")
st.write("Try to 'hack' the AI or test a normal transaction by inputting custom data below!")

# URL Render của bạn
API_URL = "https://fraudguard-project.onrender.com/predict"

# --- TẠO FORM NHẬP LIỆU (MANUAL INPUT) ---
st.subheader("🕵️‍♂️ Manual Transaction Entry")

with st.form("manual_input_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Ô nhập số tiền (Mặc định 150 đô)
        amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=150.0, step=10.0)
    with col2:
        # Ô nhập thời gian
        time = st.number_input("Time (Seconds from 0)", min_value=0.0, value=3600.0, step=60.0)

    # Dùng Expander để giấu các thông số phức tạp đi cho đỡ rối mắt
    with st.expander("⚙️ Advanced AI Features (V1 - V28)"):
        st.write("Tip from SHAP Explainer: To simulate a hacker, try sliding **V14** into deep negative numbers!")
        
        # Thanh trượt cho 3 thông số quan trọng nhất
        v14 = st.slider("V14 (Most important)", min_value=-20.0, max_value=20.0, value=0.5)
        v4 = st.slider("V4", min_value=-10.0, max_value=10.0, value=1.0)
        v12 = st.slider("V12", min_value=-20.0, max_value=20.0, value=0.5)

    # Nút Bấm Gửi
    submit_button = st.form_submit_button("🔍 Check Transaction", use_container_width=True)

# --- XỬ LÝ KHI NGƯỜI DÙNG BẤM NÚT ---
if submit_button:
    # Gom dữ liệu lại thành 1 cục (Các V khác cho bằng 0)
    custom_tx = {
        "Time": time, "V1": 0.0, "V2": 0.0, "V3": 0.0, "V4": v4, "V5": 0.0,
        "V6": 0.0, "V7": 0.0, "V8": 0.0, "V9": 0.0, "V10": 0.0, "V11": 0.0,
        "V12": v12, "V13": 0.0, "V14": v14, "V15": 0.0, "V16": 0.0, "V17": 0.0,
        "V18": 0.0, "V19": 0.0, "V20": 0.0, "V21": 0.0, "V22": 0.0, "V23": 0.0,
        "V24": 0.0, "V25": 0.0, "V26": 0.0, "V27": 0.0, "V28": 0.0,
        "Amount": amount
    }

    # Hiệu ứng loading vòng xoay tuyệt đẹp
    with st.spinner("AI is analyzing transaction patterns..."):
        try:
            # Gửi sang Render
            response = requests.post(API_URL, json=custom_tx)
            result = response.json()
            
            # In kết quả
            st.markdown("---")
            if result["prediction"] == "FRAUD":
                st.error(f"🚨 **ALERT! FRAUD DETECTED:** {result['message']}")
            else:
                st.success(f"✅ **APPROVED:** {result['message']}")
                
        except Exception as e:
            st.error(f"Connection Error: {e}. Is your Render server awake?")