import pandas as pd
import json
import time
from kafka import KafkaProducer

print("🔌 Connecting to Kafka Server...")

# 1. Setup the Producer to talk to our Docker container on port 9092
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8') # Converts data to JSON format before sending
)

print("📊 Loading transaction data from CSV...")
df = pd.read_csv("data/creditcard.csv")

# We drop the 'Class' column because in the real world, the bank doesn't know if it's fraud yet!
if 'Class' in df.columns:
    df = df.drop(columns=['Class'])

print("🚀 Starting real-time transaction stream! (Press Ctrl+C to stop)")
time.sleep(2)

# 2. Loop through the dataset and send transactions one by one
try:
    for index, row in df.iterrows():
        # Convert the row of data into a Python dictionary
        transaction = row.to_dict()
        
        # Put the transaction onto the conveyor belt lane named 'fraud_stream'
        producer.send('fraud_stream', value=transaction)
        
        print(f"[SENT] Transaction {index} | Amount: ${transaction['Amount']} | Time: {transaction['Time']}")
        
        # Pause for 0.1 seconds (Simulating 10 transactions per second happening globally)
        time.sleep(0.1) 

except KeyboardInterrupt:
    print("\n🛑 Streaming stopped by user.")
finally:
    # Ensure all data is sent before closing
    producer.flush()
    producer.close()