# 🛡️ FraudGuard: Real-Time Credit Card Fraud Detection System

An end-to-end Machine Learning pipeline that detects credit card fraud in real-time. This project handles highly imbalanced data and simulates a production-grade banking environment using modern Data Engineering and MLOps tools.

## 🚀 Architecture & Tech Stack
* **Machine Learning:** Scikit-Learn (Random Forest), SHAP (Explainable AI), Pandas
* **Data Engineering:** Snowflake (Cloud Data Warehouse), Databricks/PySpark (Big Data ETL)
* **Real-Time Streaming:** Apache Kafka (Confluent), Docker Compose
* **API & Deployment:** FastAPI, Docker (Containerization)
* **Frontend/Dashboard:** Streamlit

## 🧠 The Machine Learning Model
The dataset contains 284,807 transactions, but only **0.17% are fraudulent**. 
To handle this extreme Data Imbalance:
* Tested Logistic Regression (with class weights) and Random Forest.
* Selected **Random Forest** due to its superior Precision-Recall balance.
* **Explainability:** Implemented `SHAP` values to open the "black box", revealing that feature `V14` is the most critical indicator of fraud.

## ⚙️ System Workflow
1. **Producer:** `kafka_producer.py` streams live transactions into Apache Kafka at 10 msgs/sec.
2. **Streaming Engine:** Kafka acts as the high-speed message broker running in a Docker container.
3. **Backend API:** FastAPI runs inside a Docker container, holding the trained Random Forest model in memory to score transactions in milliseconds.
4. **Consumer UI:** A live Streamlit dashboard pulls from the Kafka stream, hits the API, and visualizes the results globally in real-time.

## 📸 Demo
*(Record a 15-second screen recording of your Streamlit live dashboard running, turn it into a GIF, and drag-and-drop it right here!)*

## 🛠️ How to run locally
1. **Start Kafka & API Containers:**
   ```bash
   docker-compose up -d
   docker build -t fraud-api-image .
   docker run -p 8080:8000 fraud-api-image