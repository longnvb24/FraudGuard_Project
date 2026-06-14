
import json
import requests
from kafka import KafkaConsumer

# This is the address of your AI Waiter (FastAPI running in Docker)
API_URL = "http://127.0.0.1:8080/predict"

print("🎧 Starting Kafka Consumer...")
print("Listening for incoming transactions on 'fraud_stream'...")

# 1. Setup the Consumer to read from the Kafka conveyor belt
consumer = KafkaConsumer(
    'fraud_stream',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest', # Only read new transactions, ignore old ones
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# 2. Continuously listen for new messages
for message in consumer:
    transaction = message.value
    
    try:
        # 3. Send the transaction to your FastAPI Docker Container
        response = requests.post(API_URL, json=transaction)
        
        # Parse the AI's answer
        result = response.json()
        
        # 4. Display the AI's decision
        if result["prediction"] == "FRAUD":
            print(f"🚨 ALERT! FRAUD BLOCKED | Amount: ${transaction['Amount']} | Time: {transaction['Time']}")
        else:
            print(f"✅ Approved | Amount: ${transaction['Amount']}")
            
    except Exception as e:
        print(f"❌ Error connecting to AI API. Is your Docker container running? Error: {e}")