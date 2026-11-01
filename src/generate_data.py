import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data():
    os.makedirs('data/input', exist_ok=True)
    np.random.seed(42) # Fixed seed for reproducible data

    print("Generating 100,000 records. This might take a few seconds...")

    num_records = 100000
    customer_ids = [f"C{i:06d}" for i in range(1, num_records + 1)]
    emails = [f"user{i}@test.com" for i in range(1, num_records + 1)]
    names = [f"User_{i}" for i in range(1, num_records + 1)]
    dates = [(datetime(2023,1,1) + timedelta(minutes=i)).isoformat() for i in range(num_records)]

    customers = pd.DataFrame({
        'customer_id': customer_ids,
        'email': emails,
        'name': names,
        'updated_at': dates
    })

    # Inject 500 duplicates (same email, newer date) to test deduplication
    for i in range(500):
        customers.loc[i, 'email'] = customers.loc[i+500, 'email']
        customers.loc[i, 'updated_at'] = datetime(2024,1,1).isoformat() 
        
    # Inject 500 nulls (missing emails) to test quarantine
    customers.loc[1000:1500, 'email'] = None

    # Generate Accounts (1 per customer)
    accounts = pd.DataFrame({
        'account_id': [f"A{i:06d}" for i in range(1, num_records + 1)],
        'customer_id': customer_ids,
        'balance': np.random.uniform(0, 10000, num_records)
    })

    customers.to_csv('data/input/customers.csv', index=False)
    accounts.to_csv('data/input/accounts.csv', index=False)
    print("Synthetic data generated in data/input/")

if __name__ == "__main__":
    generate_synthetic_data()