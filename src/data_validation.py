"""
data_validation.py
==================
Performs automated integrity, domain, and consistency validation checks on clean supply chain data.
"""

import os
import pandas as pd
import numpy as np

CLEAN_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "supply_chain_clean.csv"))

def run_validation_suite(df=None):
    if df is None:
        if not os.path.exists(CLEAN_DATA_PATH):
            raise FileNotFoundError(f"Clean data not found at {CLEAN_DATA_PATH}. Run data_cleaning.py first.")
        df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=['order_date', 'shipping_date'])

    print(f"Running validation suite on {len(df):,} records...")
    results = {}

    # 1. Primary Key Uniqueness
    unique_items = df['order_item_id'].nunique()
    total_rows = len(df)
    results['pk_uniqueness'] = (unique_items == total_rows)
    print(f"[{'PASS' if results['pk_uniqueness'] else 'FAIL'}] PK Uniqueness: {unique_items:,} unique item IDs for {total_rows:,} rows.")

    # 2. Critical Fields Null Check
    critical_cols = ['order_id', 'order_item_id', 'customer_id', 'product_id', 
                     'order_date', 'shipping_date', 'net_sales', 'profit', 'shipping_mode', 'delivery_status']
    null_counts = df[critical_cols].isnull().sum().to_dict()
    results['null_check'] = all(v == 0 for v in null_counts.values())
    print(f"[{'PASS' if results['null_check'] else 'FAIL'}] Critical Fields Null Check: {null_counts}")

    # 3. Chronological Consistency
    invalid_dates = (df['order_date'] > df['shipping_date']).sum()
    results['date_sequence'] = (invalid_dates == 0)
    print(f"[{'PASS' if results['date_sequence'] else 'FAIL'}] Date Chronology: {invalid_dates} records where order_date > shipping_date.")

    # 4. Financial Calculations Integrity
    gross_calc = (df['order_item_product_price'] * df['order_item_quantity']).round(2)
    gross_diff = (df['gross_sales'] - gross_calc).abs().max()
    results['gross_sales_identity'] = (gross_diff < 0.05)
    print(f"[{'PASS' if results['gross_sales_identity'] else 'FAIL'}] Gross Sales Identity: Max discrepancy = ${gross_diff:.4f}")

    net_calc = (df['gross_sales'] - df['order_item_discount']).round(2)
    net_diff = (df['net_sales'] - net_calc).abs().max()
    results['net_sales_identity'] = (net_diff < 0.05)
    print(f"[{'PASS' if results['net_sales_identity'] else 'FAIL'}] Net Sales Identity: Max discrepancy = ${net_diff:.4f}")

    # 5. Domain Validations
    qty_valid = (df['order_item_quantity'] > 0).all()
    results['positive_quantity'] = qty_valid
    print(f"[{'PASS' if results['positive_quantity'] else 'FAIL'}] Positive Item Quantities: {qty_valid}")

    shipping_real_valid = (df['shipping_days_real'] >= 0).all()
    results['valid_shipping_days'] = shipping_real_valid
    print(f"[{'PASS' if results['valid_shipping_days'] else 'FAIL'}] Non-Negative Shipping Days: {shipping_real_valid}")

    # 6. Delivery Status Consistency for Completed Deliveries
    on_time_mismatch = ((df['delivery_status'] == 'Shipping on time') & (df['delay_days'] != 0)).sum()
    advance_mismatch = ((df['delivery_status'] == 'Advance shipping') & (df['delay_days'] >= 0)).sum()
    late_mismatch = ((df['delivery_status'] == 'Late delivery') & (df['delay_days'] <= 0)).sum()
    delivery_status_consistent = (on_time_mismatch == 0 and advance_mismatch == 0 and late_mismatch == 0)
    results['delivery_status_logic'] = delivery_status_consistent
    print(f"[{'PASS' if results['delivery_status_logic'] else 'FAIL'}] Delivery Status Logic: on_time err={on_time_mismatch}, adv err={advance_mismatch}, late err={late_mismatch}")

    all_passed = all(results.values())
    print(f"\nOverall Validation Result: {'ALL TESTS PASSED' if all_passed else 'SOME CHECKS FAILED'}")
    return results

if __name__ == "__main__":
    run_validation_suite()
