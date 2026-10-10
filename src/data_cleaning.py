"""
data_cleaning.py
================
Standardizes, cleans, and normalizes the DataCo Smart Supply Chain dataset.
Produces clean analytical data frames and exports to data/processed/.
"""

import os
import pandas as pd
import numpy as np

RAW_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "DataCoSupplyChainDataset.csv"))
PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))

COLUMN_RENAME_MAP = {
    'Type': 'payment_type',
    'Days for shipping (real)': 'shipping_days_real',
    'Days for shipment (scheduled)': 'shipping_days_scheduled',
    'Benefit per order': 'benefit_per_order',
    'Sales per customer': 'sales_per_customer',
    'Delivery Status': 'delivery_status',
    'Late_delivery_risk': 'late_delivery_risk',
    'Category Id': 'category_id',
    'Category Name': 'category_name',
    'Customer City': 'customer_city',
    'Customer Country': 'customer_country',
    'Customer Email': 'customer_email',
    'Customer Fname': 'customer_fname',
    'Customer Id': 'customer_id',
    'Customer Lname': 'customer_lname',
    'Customer Password': 'customer_password',
    'Customer Segment': 'customer_segment',
    'Customer State': 'customer_state',
    'Customer Street': 'customer_street',
    'Customer Zipcode': 'customer_zipcode',
    'Department Id': 'department_id',
    'Department Name': 'department_name',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
    'Market': 'market',
    'Order City': 'order_city',
    'Order Country': 'order_country',
    'Order Customer Id': 'order_customer_id',
    'order date (DateOrders)': 'order_date',
    'Order Id': 'order_id',
    'Order Item Cardprod Id': 'order_item_cardprod_id',
    'Order Item Discount': 'order_item_discount',
    'Order Item Discount Rate': 'order_item_discount_rate',
    'Order Item Id': 'order_item_id',
    'Order Item Product Price': 'order_item_product_price',
    'Order Item Profit Ratio': 'order_item_profit_ratio',
    'Order Item Quantity': 'order_item_quantity',
    'Sales': 'gross_sales',
    'Order Item Total': 'net_sales',
    'Order Profit Per Order': 'profit',
    'Order Region': 'order_region',
    'Order State': 'order_state',
    'Order Status': 'order_status',
    'Order Zipcode': 'order_zipcode',
    'Product Card Id': 'product_id',
    'Product Category Id': 'product_category_id',
    'Product Description': 'product_description',
    'Product Image': 'product_image',
    'Product Name': 'product_name',
    'Product Price': 'product_price',
    'Product Status': 'product_status',
    'shipping date (DateOrders)': 'shipping_date',
    'Shipping Mode': 'shipping_mode'
}

def load_raw_data(filepath=RAW_DATA_PATH):
    print(f"Loading raw dataset from {filepath} with encoding 'latin1'...")
    df = pd.read_csv(filepath, encoding='latin1')
    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns.")
    return df

def clean_dataset(df):
    print("Beginning cleaning and standardization...")
    df_clean = df.rename(columns=COLUMN_RENAME_MAP).copy()

    # Drop 100% null columns and uninformative metadata
    cols_to_drop = ['product_description', 'customer_password', 'customer_email', 'product_image']
    existing_drops = [c for c in cols_to_drop if c in df_clean.columns]
    df_clean.drop(columns=existing_drops, inplace=True)
    print(f"Dropped uninformative/sensitive columns: {existing_drops}")

    # Impute minor nulls
    df_clean['customer_lname'] = df_clean['customer_lname'].fillna('Unknown').str.strip()
    df_clean['customer_fname'] = df_clean['customer_fname'].fillna('Unknown').str.strip()
    df_clean['customer_zipcode'] = df_clean['customer_zipcode'].fillna(0).astype(int).astype(str)
    df_clean['order_zipcode'] = df_clean['order_zipcode'].fillna('Unknown').astype(str)

    # Clean textual fields
    text_cols = ['category_name', 'department_name', 'customer_city', 'customer_state',
                 'order_city', 'order_state', 'order_region', 'order_country',
                 'market', 'shipping_mode', 'delivery_status', 'order_status', 'product_name']
    for col in text_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    # Parse Dates
    print("Parsing date columns...")
    df_clean['order_date'] = pd.to_datetime(df_clean['order_date'])
    df_clean['shipping_date'] = pd.to_datetime(df_clean['shipping_date'])

    # Numeric Casts and Sanity Checks
    numeric_floats = ['gross_sales', 'net_sales', 'profit', 'order_item_discount', 
                      'order_item_discount_rate', 'order_item_product_price', 'product_price']
    for nf in numeric_floats:
        df_clean[nf] = pd.to_numeric(df_clean[nf], errors='coerce').round(2)

    numeric_ints = ['shipping_days_real', 'shipping_days_scheduled', 'order_item_quantity',
                    'order_id', 'order_item_id', 'customer_id', 'product_id', 'category_id', 'department_id']
    for ni in numeric_ints:
        df_clean[ni] = df_clean[ni].astype(int)

    # Derived Operational Flags
    df_clean['delay_days'] = df_clean['shipping_days_real'] - df_clean['shipping_days_scheduled']
    df_clean['is_delayed'] = (df_clean['delay_days'] > 0).astype(int)
    df_clean['is_late_delivery'] = (df_clean['delivery_status'] == 'Late delivery').astype(int)
    df_clean['is_eligible_shipment'] = (df_clean['delivery_status'] != 'Shipping canceled').astype(int)
    
    # Margin calculation
    df_clean['profit_margin'] = np.where(
        df_clean['net_sales'] > 0,
        (df_clean['profit'] / df_clean['net_sales']).round(4),
        0.0
    )

    print(f"Cleaning complete. Output shape: {df_clean.shape}")
    return df_clean

def save_clean_data(df_clean, output_dir=PROCESSED_DIR):
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "supply_chain_clean.csv")
    print(f"Exporting clean master dataset to {out_file}...")
    df_clean.to_csv(out_file, index=False, encoding='utf-8')
    print("Master clean dataset successfully saved.")
    return out_file

if __name__ == "__main__":
    raw_df = load_raw_data()
    cleaned_df = clean_dataset(raw_df)
    save_clean_data(cleaned_df)
