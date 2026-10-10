"""
test_metrics.py
===============
Automated tests verifying mathematical and business logic of analytical KPIs.
"""

import os
import pytest
import pandas as pd
import numpy as np

CLEAN_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "supply_chain_clean.csv"))

@pytest.fixture(scope="module")
def clean_data():
    return pd.read_csv(CLEAN_DATA_PATH)

def test_gross_sales_calculation(clean_data):
    """Gross sales must equal quantity * unit product price."""
    calc_gross = (clean_data['order_item_product_price'] * clean_data['order_item_quantity']).round(2)
    max_diff = (clean_data['gross_sales'] - calc_gross).abs().max()
    assert max_diff < 0.05, f"Discrepancy in gross sales: {max_diff}"

def test_net_sales_calculation(clean_data):
    """Net sales must equal gross sales minus discount."""
    calc_net = (clean_data['gross_sales'] - clean_data['order_item_discount']).round(2)
    max_diff = (clean_data['net_sales'] - calc_net).abs().max()
    assert max_diff < 0.05, f"Discrepancy in net sales: {max_diff}"

def test_delivery_eligibility_denominator(clean_data):
    """Eligible shipments must exclude canceled shipments."""
    total_rows = len(clean_data)
    canceled_rows = (clean_data['delivery_status'] == 'Shipping canceled').sum()
    eligible_rows = clean_data['is_eligible_shipment'].sum()
    assert eligible_rows == (total_rows - canceled_rows), "Eligible shipment count mismatch"

def test_late_delivery_rate_bounds(clean_data):
    """Eligible late delivery rate must be between 0% and 100%."""
    eligible = clean_data[clean_data['is_eligible_shipment'] == 1]
    late_count = (eligible['delivery_status'] == 'Late delivery').sum()
    late_rate = late_count / len(eligible)
    assert 0.0 <= late_rate <= 1.0, f"Invalid late delivery rate: {late_rate}"
    assert np.isclose(late_rate, 0.5729, atol=0.001), f"Unexpected late rate value: {late_rate}"

def test_on_time_complement(clean_data):
    """On-time rate + Late rate must equal 100% on eligible shipments."""
    eligible = clean_data[clean_data['is_eligible_shipment'] == 1]
    late_rate = (eligible['delivery_status'] == 'Late delivery').mean()
    on_time_rate = (eligible['delivery_status'].isin(['Advance shipping', 'Shipping on time'])).mean()
    assert np.isclose(late_rate + on_time_rate, 1.0, atol=1e-5), "On-time and late rates do not sum to 1.0"
