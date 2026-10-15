"""
export_star_schema.py
======================
Generates and saves the exact Star Schema CSVs in data/processed/ according to the project specification.
"""

import os
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "supply_chain_clean.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")

def export_all():
    print(f"Reading clean data from {CLEAN_DATA_PATH}...")
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=['order_date', 'shipping_date'])

    # 1. DimDate
    print("Exporting dim_date.csv...")
    min_date = min(df['order_date'].min(), df['shipping_date'].min())
    max_date = max(df['order_date'].max(), df['shipping_date'].max())
    date_range = pd.date_range(start=min_date.date(), end=max_date.date(), freq='D')
    dim_date = pd.DataFrame({
        'date_key': date_range.strftime('%Y%m%d').astype(int),
        'full_date': date_range.strftime('%Y-%m-%d'),
        'year': date_range.year,
        'quarter': date_range.quarter,
        'month': date_range.month,
        'month_name': date_range.strftime('%B'),
        'year_month': date_range.strftime('%Y-%m'),
        'week': date_range.isocalendar().week.astype(int),
        'day_of_week': date_range.dayofweek + 1,
        'day_name': date_range.strftime('%A'),
        'is_weekend': date_range.dayofweek.isin([5, 6]).astype(int)
    })
    dim_date.to_csv(os.path.join(OUTPUT_DIR, "dim_date.csv"), index=False)

    # 2. DimShipping
    print("Exporting dim_shipping.csv...")
    dim_shipping = df[['shipping_mode', 'delivery_status']].drop_duplicates().sort_values(['shipping_mode', 'delivery_status']).reset_index(drop=True)
    dim_shipping['shipping_id'] = range(1, len(dim_shipping) + 1)
    dim_shipping = dim_shipping[['shipping_id', 'shipping_mode', 'delivery_status']]
    dim_shipping.to_csv(os.path.join(OUTPUT_DIR, "dim_shipping.csv"), index=False)

    # 3. DimGeography
    print("Exporting dim_geography.csv...")
    dim_geo = df.groupby(['market', 'order_region', 'order_country', 'order_state', 'order_city'], as_index=False).agg({'latitude': 'first', 'longitude': 'first'})
    dim_geo['geo_id'] = range(1, len(dim_geo) + 1)
    dim_geo = dim_geo[['geo_id', 'market', 'order_region', 'order_country', 'order_state', 'order_city', 'latitude', 'longitude']]
    dim_geo.to_csv(os.path.join(OUTPUT_DIR, "dim_geography.csv"), index=False)

    # 4. DimCustomer
    print("Exporting dim_customer.csv...")
    dim_customer = df[['customer_id', 'customer_fname', 'customer_lname', 'customer_segment', 'customer_city', 'customer_state', 'customer_country', 'customer_street', 'customer_zipcode']].drop_duplicates(subset=['customer_id']).sort_values('customer_id').reset_index(drop=True)
    dim_customer.to_csv(os.path.join(OUTPUT_DIR, "dim_customer.csv"), index=False)

    # 5. DimOrder
    print("Exporting dim_order.csv...")
    dim_order = df[['order_id', 'order_status', 'payment_type']].drop_duplicates(subset=['order_id']).sort_values('order_id').reset_index(drop=True)
    dim_order.to_csv(os.path.join(OUTPUT_DIR, "dim_order.csv"), index=False)

    # 6. DimProduct
    print("Exporting dim_product.csv...")
    dim_product = df[['product_id', 'product_name', 'product_price', 'category_id', 'category_name', 'department_id', 'department_name']].drop_duplicates(subset=['product_id']).sort_values('product_id').reset_index(drop=True)
    dim_product.to_csv(os.path.join(OUTPUT_DIR, "dim_product.csv"), index=False)

    # 7. FactOrderItems
    print("Exporting fact_order_items.csv...")
    df_fact = df.merge(dim_geo[['market', 'order_region', 'order_country', 'order_state', 'order_city', 'geo_id']], on=['market', 'order_region', 'order_country', 'order_state', 'order_city'], how='left')
    df_fact = df_fact.merge(dim_shipping[['shipping_mode', 'delivery_status', 'shipping_id']], on=['shipping_mode', 'delivery_status'], how='left')
    df_fact['order_date_key'] = df_fact['order_date'].dt.strftime('%Y%m%d').astype(int)
    df_fact['shipping_date_key'] = df_fact['shipping_date'].dt.strftime('%Y%m%d').astype(int)
    df_fact['sales'] = df_fact['net_sales']
    df_fact['order_profit_per_order'] = df_fact['benefit_per_order']
    df_fact['days_for_shipping_real'] = df_fact['shipping_days_real']
    df_fact['days_for_shipment_scheduled'] = df_fact['shipping_days_scheduled']

    fact_cols = [
        'order_item_id', 'order_id', 'order_date_key', 'shipping_date_key',
        'customer_id', 'product_id', 'geo_id', 'shipping_id',
        'order_item_quantity', 'sales', 'order_item_discount', 'order_item_discount_rate',
        'order_item_product_price', 'order_item_profit_ratio', 'order_profit_per_order',
        'benefit_per_order', 'sales_per_customer', 'days_for_shipping_real',
        'days_for_shipment_scheduled', 'late_delivery_risk'
    ]
    fact = df_fact[fact_cols]
    fact.to_csv(os.path.join(OUTPUT_DIR, "fact_order_items.csv"), index=False)
    print("All Star Schema CSV files exported successfully!")

if __name__ == "__main__":
    export_all()
