from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Initialize the FastAPI
app = FastAPI(title="FraudGuard API", description="Real-time Credit Card Fraud Detection")

# 2. Load the the models saved earlier
print("Loading the Random Forest model and Scaler...")
rf_model = joblib.load('models/random_forest_fraud_model.pkl')
scaler = joblib.load('models/scaler.pkl')
print("Models loaded successfully!")

# 3. Use Pydantic to ensure the input data is strictly formatted.
class Transaction(BaseModel):
    Time: float
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float
    Amount: float

# 4. Create the "Endpoint"
@app.post("/predict")
def predict_fraud(transaction: Transaction):
    # Convert the received JSON data into a Python dictionary, then to a Pandas DataFrame
    data_dict = transaction.dict()
    df = pd.DataFrame([data_dict])
    
    # Preprocessing: Scale the 'Time' and 'Amount' exactly like we did in training
    df[['Time', 'Amount']] = scaler.transform(df[['Time', 'Amount']])
    
    # Ask the AI to make a prediction
    prediction = rf_model.predict(df) # Returns [0] or [1]
    
    # Check the result
    is_fraud = bool(prediction[0] == 1)
    
    # Return the answer to the user
    if is_fraud:
        return {"status": "success", "prediction": "FRAUD", "message": "Transaction blocked!"}
    else:
        return {"status": "success", "prediction": "NORMAL", "message": "Transaction approved."}

# A simple health check endpoint
@app.get("/")
def health_check():
    return {"message": "FraudGuard API is running perfectly!"}