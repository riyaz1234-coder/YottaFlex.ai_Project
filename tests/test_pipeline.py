import pandas as pd
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from pipeline import deduplicate_customers, validate_and_quarantine

def test_deduplication_happy_path():
    df = pd.DataFrame({
        'id': ['C1', 'C2'],
        'email': ['test@test.com', 'test@test.com'],
        'name': ['A', 'B'],
        'updated': ['2023-01-01', '2023-01-02']
    })
    result = deduplicate_customers(df)
    assert len(result) == 1
    assert result.iloc[0]['id'] == 'C2' 

def test_validation_quarantine_nulls():
    df = pd.DataFrame({
        'id': ['C1', 'C2'],
        'email': ['valid@test.com', None],
        'name': ['A', 'B'],
        'updated': ['2023-01-01', '2023-01-01']
    })
    valid, rejected = validate_and_quarantine(df, run_id="test_run")
    assert len(valid) == 1
    assert len(rejected) == 1

def test_empty_input():
    df = pd.DataFrame(columns=['id', 'email', 'name', 'updated'])
    valid, rejected = validate_and_quarantine(df, run_id="test_run")
    assert len(valid) == 0
    assert len(rejected) == 0