"""
test_aggregation.py
===================
Automated tests verifying order vs item aggregation grains,
relational foreign key referential integrity, and Python-to-SQL reconciliation.
"""

import os
import pytest
import pandas as pd
import numpy as np

PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))

@pytest.fixture(scope="module")
def star_schema():
    fact = pd.read_csv(os.path.join(PROCESSED_DIR, "fact_order_items.csv"))
    dim_product = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_product.csv"))
    dim_customer = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_customer.csv"))
    dim_geo = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_geography.csv"))
    dim_order = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_order.csv"))
    dim_date = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_date.csv"))
    dim_shipping = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_shipping.csv"))
    return {
        'fact': fact,
        'dim_product': dim_product,
        'dim_customer': dim_customer,
        'dim_geo': dim_geo,
        'dim_order': dim_order,
        'dim_date': dim_date,
        'dim_shipping': dim_shipping
    }

def test_distinct_order_grain_ratio(star_schema):
    """Ensure distinct order count is ~65,752 and items per order is ~2.75."""
    fact = star_schema['fact']
    unique_orders = fact['order_id'].nunique()
    total_items = len(fact)
    ratio = total_items / unique_orders

    assert unique_orders == 65752, f"Expected 65,752 unique orders, got {unique_orders}"
    assert np.isclose(ratio, 2.745, atol=0.01), f"Unexpected items-per-order ratio: {ratio}"

def test_foreign_key_referential_integrity(star_schema):
    """Verify that every foreign key in the fact table exists in the dimension table."""
    fact = star_schema['fact']
    
    # 1. Product FK
    invalid_prods = set(fact['product_id']) - set(star_schema['dim_product']['product_id'])
    assert len(invalid_prods) == 0, f"Found orphaned product foreign keys: {invalid_prods}"

    # 2. Customer FK
    invalid_custs = set(fact['customer_id']) - set(star_schema['dim_customer']['customer_id'])
    assert len(invalid_custs) == 0, f"Found orphaned customer foreign keys: {invalid_custs}"

    # 3. Geography FK
    invalid_geos = set(fact['geo_id']) - set(star_schema['dim_geo']['geo_id'])
    assert len(invalid_geos) == 0, f"Found orphaned geography foreign keys: {invalid_geos}"

    # 4. Shipping FK
    invalid_ships = set(fact['shipping_id']) - set(star_schema['dim_shipping']['shipping_id'])
    assert len(invalid_ships) == 0, f"Found orphaned shipping foreign keys: {invalid_ships}"

    # 5. Order FK
    invalid_orders = set(fact['order_id']) - set(star_schema['dim_order']['order_id'])
    assert len(invalid_orders) == 0, f"Found orphaned order foreign keys: {invalid_orders}"

    # 6. Order Date FK
    invalid_dates = set(fact['order_date_key']) - set(star_schema['dim_date']['date_key'])
    assert len(invalid_dates) == 0, f"Found orphaned date foreign keys: {invalid_dates}"

def test_python_to_sql_total_reconciliation(star_schema):
    """Ensure benchmark totals match exact verified SQL results."""
    fact = star_schema['fact']
    
    total_sales = fact['sales'].sum().round(2)
    total_profit = fact['benefit_per_order'].sum().round(2)
    late_count = fact['late_delivery_risk'].sum()

    assert np.isclose(total_sales, 33054402.04, atol=0.05), f"Sales mismatch: {total_sales}"
    assert np.isclose(total_profit, 3966907.39, atol=0.05), f"Profit mismatch: {total_profit}"
    assert late_count == 98977, f"Late count mismatch: {late_count}"
