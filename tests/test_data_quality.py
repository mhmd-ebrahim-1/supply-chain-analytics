"""
test_data_quality.py
====================
Automated test suite verifying dataset integrity, primary keys, and data domain constraints.
"""

import os
import pytest
import pandas as pd
import numpy as np

CLEAN_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "supply_chain_clean.csv"))

@pytest.fixture(scope="module")
def clean_data():
    if not os.path.exists(CLEAN_DATA_PATH):
        pytest.fail(f"Clean dataset missing at {CLEAN_DATA_PATH}. Run pipeline first.")
    return pd.read_csv(CLEAN_DATA_PATH, parse_dates=['order_date', 'shipping_date'])

def test_record_count(clean_data):
    """Verify exact expected record volume."""
    assert len(clean_data) == 180519, f"Expected 180,519 rows, found {len(clean_data):,}"

def test_primary_key_uniqueness(clean_data):
    """Ensure order_item_id is strictly unique."""
    assert clean_data['order_item_id'].nunique() == len(clean_data), "order_item_id is not unique"

def test_critical_non_nulls(clean_data):
    """Ensure zero nulls in essential foreign keys and metrics."""
    critical_cols = ['order_id', 'order_item_id', 'customer_id', 'product_id', 
                     'order_date', 'shipping_date', 'net_sales', 'profit', 'shipping_mode']
    for col in critical_cols:
        assert clean_data[col].isnull().sum() == 0, f"Column {col} contains unexpected nulls"

def test_date_chronology(clean_data):
    """Ensure order_date never occurs after shipping_date."""
    inversions = (clean_data['order_date'] > clean_data['shipping_date']).sum()
    assert inversions == 0, f"Detected {inversions} records where order_date > shipping_date"

def test_positive_quantities(clean_data):
    """Ensure all item quantities are strictly positive."""
    assert (clean_data['order_item_quantity'] > 0).all(), "Found non-positive item quantities"

def test_valid_shipping_duration(clean_data):
    """Ensure scheduled and real shipping days are non-negative."""
    assert (clean_data['shipping_days_real'] >= 0).all(), "Negative actual shipping days detected"
    assert (clean_data['shipping_days_scheduled'] >= 0).all(), "Negative scheduled shipping days detected"
