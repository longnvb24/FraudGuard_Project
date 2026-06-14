import snowflake.connector
import pandas as pd

print("Connecting to Snowflake Cloud...")

# Replace these with your actual details!
conn = snowflake.connector.connect(
    user='LONGNVB24',             # Usually the username you created (all caps or exact match)
    password='Longntb24112003',         # Your Snowflake password
    account='KIZYOKO-XU04751',
    warehouse='FRAUD_WH',
    database='FRAUD_DB',
    schema='FRAUD_SCHEMA'
)

print("✅ Successfully connected to Snowflake!")

# Let's ask Snowflake for the first 5 transactions and some basic stats
print("Fetching data from the cloud...")

query = """
    SELECT 
        COUNT(*) as total_transactions,
        SUM(Class) as total_frauds
    FROM transactions;
"""

# Fetch the data into a Pandas DataFrame
df = pd.read_sql(query, conn)

print("\n--- SNOWFLAKE DATA SUMMARY ---")
print(df)

# Always close the connection when done
conn.close()