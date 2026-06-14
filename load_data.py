import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:24112003@localhost:5432/fraud_db"

def load_data_to_db():
    print("Loading CSV file...")
    df = pd.read_csv("data/creditcard.csv")
    print(f"Loading finished! The dataset have {df.shape[0]} rows and {df.shape[1]} columns")

    print("Connecting to PostgreSQL...")

    engine = create_engine(DB_URL)

    print("Loading data into the database...")

    df.to_sql("transactions", engine, if_exists='replace', index=False)

    print("Success! Open pgAdmin to check!")

if __name__ == "__main__":
    load_data_to_db()