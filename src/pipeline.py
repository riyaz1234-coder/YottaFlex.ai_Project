import pandas as pd
import uuid
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_run_id():
    return str(uuid.uuid4())

def validate_and_quarantine(customers_df, run_id):
    valid_mask = customers_df['email'].notnull() & customers_df['name'].notnull()
    valid_df = customers_df[valid_mask].copy()
    
    rejected_df = customers_df[~valid_mask].copy()
    if not rejected_df.empty:
        rejected_df['reject_reason'] = 'Missing field'
        rejected_df['run_id'] = run_id
        os.makedirs('data/quarantine', exist_ok=True)
        rejected_df.to_csv(f'data/quarantine/rejected_{run_id}.csv', index=False)
    
    return valid_df, rejected_df

def deduplicate_customers(customers_df):
    # Uses the new 'updated' column
    customers_df['updated'] = pd.to_datetime(customers_df['updated'])
    deduped_df = customers_df.sort_values('updated').drop_duplicates(subset=['email'], keep='last')
    return deduped_df

def execute_pipeline():
    run_id = get_run_id()
    logging.info(f"Starting Pipeline Run ID: {run_id}")

    try:
        customers_df = pd.read_csv('data/input/customers.csv')
        accounts_df = pd.read_csv('data/input/accounts.csv')
        input_count = len(customers_df)

        valid_cust, rejected_cust = validate_and_quarantine(customers_df, run_id)
        deduped_cust = deduplicate_customers(valid_cust)
        
        # Merges using the new 'id' column
        unified_df = pd.merge(deduped_cust, accounts_df, on='id', how='left')
        
        # Keep only run_id to save space
        unified_df['run_id'] = run_id

        os.makedirs('data/output', exist_ok=True)
        output_path = f'data/output/unified_view_{run_id}.csv'
        unified_df.to_csv(output_path, index=False)

        logging.info(f"SUCCESS. Input: {input_count} | Output: {len(unified_df)} | Rejected: {len(rejected_cust)}")
        
    except Exception as e:
        logging.error(f"Pipeline Failed: {str(e)}")
        raise