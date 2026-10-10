"""
feature_engineering.py
======================
Generates analytical features and extracts normalized Star Schema tables
(FactOrderItems, DimDate, DimProduct, DimCustomer, DimGeography, DimShipping, DimOrder).
"""

import os
import pandas as pd
import numpy as np

CLEAN_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "supply_chain_clean.csv"))
PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))

def engineer_features(df):
    print("Engineering analytical features...")
    
    # 1. Temporal Dimensions
    df['order_year'] = df['order_date'].dt.year
    df['order_month'] = df['order_date'].dt.month
    df['order_year_month'] = df['order_date'].dt.strftime('%Y-%m')
    df['order_day_of_week'] = df['order_date'].dt.day_name()
    df['order_hour'] = df['order_date'].dt.hour
    df['order_date_only'] = df['order_date'].dt.date
    
    df['shipping_year_month'] = df['shipping_date'].dt.strftime('%Y-%m')
    df['shipping_date_only'] = df['shipping_date'].dt.date

    # 2. Discount Tiers
    discount_bins = [-0.01, 0.00, 0.10, 0.18, 1.0]
    discount_labels = ['No Discount (0%)', 'Low (1-10%)', 'Moderate (11-18%)', 'High (>18%)']
    df['discount_tier'] = pd.cut(df['order_item_discount_rate'], bins=discount_bins, labels=discount_labels)

    # 3. Product ABC Classification (by Net Revenue)
    prod_rev = df.groupby('product_id')['net_sales'].sum().reset_index()
    prod_rev = prod_rev.sort_values(by='net_sales', ascending=False)
    prod_rev['cumulative_revenue'] = prod_rev['net_sales'].cumsum()
    total_rev = prod_rev['net_sales'].sum()
    prod_rev['cum_pct'] = prod_rev['cumulative_revenue'] / total_rev
    
    def assign_abc(pct):
        if pct <= 0.70:
            return 'Class A (Top 70%)'
        elif pct <= 0.90:
            return 'Class B (Next 20%)'
        else:
            return 'Class C (Bottom 10%)'
            
    prod_rev['abc_revenue_class'] = prod_rev['cum_pct'].apply(assign_abc)
    df = df.merge(prod_rev[['product_id', 'abc_revenue_class']], on='product_id', how='left')

    # 4. Regional Late Severity
    region_late = df[df['is_eligible_shipment'] == 1].groupby('order_region')['is_late_delivery'].mean().reset_index()
    region_late.rename(columns={'is_late_delivery': 'region_late_rate'}, inplace=True)
    df = df.merge(region_late, on='order_region', how='left')

    return df

def build_star_schema(df, output_dir=PROCESSED_DIR):
    print("Building Star Schema dimensional tables...")
    os.makedirs(output_dir, exist_ok=True)

    # 1. DimDate
    min_date = min(df['order_date_only'].min(), df['shipping_date_only'].min())
    max_date = max(df['order_date_only'].max(), df['shipping_date_only'].max())
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    dim_date = pd.DataFrame({'date_key': date_range.strftime('%Y%m%d').astype(int),
                             'full_date': date_range.date,
                             'year': date_range.year,
                             'quarter': date_range.quarter,
                             'month': date_range.month,
                             'month_name': date_range.strftime('%B'),
                             'year_month': date_range.strftime('%Y-%m'),
                             'day_of_month': date_range.day,
                             'day_of_week': date_range.day_name(),
                             'is_weekend': date_range.dayofweek.isin([5, 6]).astype(int)})
    dim_date.to_csv(os.path.join(output_dir, "dim_date.csv"), index=False)
    print(f"Created DimDate: {len(dim_date)} days.")

    # 2. DimProduct
    dim_product = df[['product_id', 'product_name', 'product_price', 'category_id', 
                      'category_name', 'department_id', 'department_name', 'abc_revenue_class']].drop_duplicates(subset=['product_id']).copy()
    dim_product.sort_values(by='product_id', inplace=True)
    dim_product.to_csv(os.path.join(output_dir, "dim_product.csv"), index=False)
    print(f"Created DimProduct: {len(dim_product)} products.")

    # 3. DimCustomer
    dim_customer = df[['customer_id', 'customer_fname', 'customer_lname', 'customer_segment',
                       'customer_city', 'customer_state', 'customer_country', 'customer_street', 'customer_zipcode']].drop_duplicates(subset=['customer_id']).copy()
    dim_customer['customer_full_name'] = dim_customer['customer_fname'] + ' ' + dim_customer['customer_lname']
    dim_customer.sort_values(by='customer_id', inplace=True)
    dim_customer.to_csv(os.path.join(output_dir, "dim_customer.csv"), index=False)
    print(f"Created DimCustomer: {len(dim_customer)} customers.")

    # 4. DimGeography (Destination Hierarchy)
    dim_geo = df[['order_region', 'order_country', 'order_state', 'order_city', 'market']].drop_duplicates().copy()
    dim_geo['geography_id'] = range(1, len(dim_geo) + 1)
    dim_geo.to_csv(os.path.join(output_dir, "dim_geography.csv"), index=False)
    print(f"Created DimGeography: {len(dim_geo)} unique geographic routes.")

    # 5. DimShipping
    dim_shipping = df[['shipping_mode', 'shipping_days_scheduled', 'delivery_status']].drop_duplicates().copy()
    dim_shipping['shipping_profile_id'] = range(1, len(dim_shipping) + 1)
    dim_shipping.to_csv(os.path.join(output_dir, "dim_shipping.csv"), index=False)
    print(f"Created DimShipping: {len(dim_shipping)} profiles.")

    # 6. DimOrder
    dim_order = df[['order_id', 'payment_type', 'order_status', 'market', 'order_region']].drop_duplicates(subset=['order_id']).copy()
    dim_order.to_csv(os.path.join(output_dir, "dim_order.csv"), index=False)
    print(f"Created DimOrder: {len(dim_order)} unique orders.")

    # 7. FactOrderItems
    # Merge keys
    df_fact = df.merge(dim_geo[['order_region', 'order_country', 'order_state', 'order_city', 'market', 'geography_id']],
                       on=['order_region', 'order_country', 'order_state', 'order_city', 'market'], how='left')
    
    df_fact['order_date_key'] = pd.to_datetime(df_fact['order_date_only']).dt.strftime('%Y%m%d').astype(int)
    df_fact['shipping_date_key'] = pd.to_datetime(df_fact['shipping_date_only']).dt.strftime('%Y%m%d').astype(int)

    fact_cols = [
        'order_item_id', 'order_id', 'customer_id', 'product_id', 'geography_id',
        'order_date_key', 'shipping_date_key', 'shipping_mode', 'delivery_status',
        'order_item_quantity', 'order_item_product_price', 'order_item_discount',
        'order_item_discount_rate', 'gross_sales', 'net_sales', 'profit', 'profit_margin',
        'shipping_days_real', 'shipping_days_scheduled', 'delay_days',
        'is_delayed', 'is_late_delivery', 'is_eligible_shipment', 'discount_tier'
    ]
    fact_order_items = df_fact[fact_cols].copy()
    fact_order_items.to_csv(os.path.join(output_dir, "fact_order_items.csv"), index=False)
    print(f"Created FactOrderItems: {len(fact_order_items)} items.")

    return True

if __name__ == "__main__":
    if not os.path.exists(CLEAN_DATA_PATH):
        from data_cleaning import load_raw_data, clean_dataset, save_clean_data
        raw = load_raw_data()
        cleaned = clean_dataset(raw)
        save_clean_data(cleaned)
    else:
        cleaned = pd.read_csv(CLEAN_DATA_PATH, parse_dates=['order_date', 'shipping_date'])
        
    df_featured = engineer_features(cleaned)
    build_star_schema(df_featured)
