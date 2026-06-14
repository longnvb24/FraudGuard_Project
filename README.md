***

# 🛡️ FraudGuard: Real-Time Credit Card Fraud Detection System

An Enterprise-grade, End-to-End Machine Learning and Data Engineering pipeline built to detect fraudulent credit card transactions in real-time. This project handles extreme data imbalance and simulates a production environment using modern MLOps and Big Data tools.

## 🚀 System Architecture & Tech Stack

The pipeline is designed with a Microservices architecture, separating storage, processing, inference, and UI.

*   **Machine Learning:** Scikit-Learn (Random Forest), SHAP (Explainable AI), Pandas.
*   **Data Engineering:** Snowflake (Cloud Data Warehouse), Databricks & PySpark (Distributed ETL).
*   **Real-Time Streaming:** Apache Kafka (Confluent Image), Docker Compose.
*   **Backend API & MLOps:** FastAPI, Docker, Uvicorn.
*   **Frontend / UI:** Streamlit (Hosted on Streamlit Community Cloud).
*   **Cloud Deployment:** Render.com (API Hosting).

## 📂 Project Structure
```text
FraudGuard_Project/
├── data/
│   └── creditcard.csv                 # Raw dataset (Ignored in Git)
├── models/
│   ├── random_forest_fraud_model.pkl  # Serialized trained model
│   └── scaler.pkl                     # Serialized StandardScaler
├── notebooks/
│   └── 1_EDA.ipynb                    # EDA, Data Imbalance handling, Training
├── src/
│   ├── api.py                         # FastAPI backend service
│   ├── test_snowflake.py              # Snowflake connection validation
│   ├── kafka_producer.py              # Simulates live transaction stream
│   └── kafka_consumer.py              # Consumes stream & hits Inference API
├── frontend/
│   ├── app.py                         # Streamlit Dashboard (Multi-tab UI)
│   └── requirements.txt               # Lightweight dependencies for UI
├── Dockerfile                         # API Containerization
├── docker-compose.yml                 # Kafka Broker configuration
├── requirements.txt                   # Backend/ML dependencies
└── README.md                          # Project Documentation
```

## 🧠 Design Decisions & Trade-offs (For Code Review Context)

1.  **Handling Data Imbalance (0.17% Fraud Rate):** 
    *   Instead of blindly applying SMOTE (which can overfit), I utilized `RandomForestClassifier(class_weight='balanced')`. Random Forest provided a superior balance between Recall (catching frauds) and Precision (minimizing false positives/customer friction).
2.  **Explainable AI (XAI):**
    *   In fintech, "Black Box" models are non-compliant. I integrated `SHAP` values to explain feature importance, identifying `V14`, `V4`, and `V12` as the key drivers for fraud detection.
3.  **Decoupled Architecture (Frontend vs Backend):**
    *   The Streamlit UI and FastAPI backend have separate `requirements.txt` files. This prevents heavy ML libraries (like `scikit-learn` or `kafka-python`) from crashing the lightweight Streamlit Cloud container, ensuring fast UI deployments.
4.  **Local to Cloud Migration:**
    *   Initially developed using local CSVs and Pandas, the data layer was migrated to **Snowflake** for scalable cloud storage, and PySpark on **Databricks** for distributed big data processing logic.

## 🛠️ How to Run Locally

### 1. Setup Environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Kafka Streaming Engine
```bash
docker-compose up -d
```

### 3. Build & Run the API (Inference Engine)
```bash
docker build -t fraud-api .
docker run -p 8080:8000 fraud-api
```
*API Docs will be available at: `http://localhost:8080/docs`*

### 4. Run the Live Stream Simulation
Open a new terminal and start the producer to send transactions to the Kafka broker:
```bash
python src/kafka_producer.py
```
Open another terminal to consume and evaluate them via the API:
```bash
python src/kafka_consumer.py
```

### 5. Start the Interactive Dashboard
```bash
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

## 🌐 Live Cloud Demo
The system has been successfully deployed to the cloud:
*   **Interactive UI (Streamlit):** https://fraudguardproject.streamlit.app/
*   **API Documentation (Render):** https://fraudguard-project.onrender.com/docs

***