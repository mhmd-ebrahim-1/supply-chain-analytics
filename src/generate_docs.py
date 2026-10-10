import json
import os

stats_path = r'D:\Downloads\supply-chain-analytics\reports\column_stats.json'
with open(stats_path, 'r', encoding='utf-8') as f:
    stats = json.load(f)

md = []
md.append('# Data Dictionary: DataCo Smart Supply Chain Dataset\n')
md.append('## 1. Overview\n')
md.append('- **Source File:** `data/raw/DataCoSupplyChainDataset.csv`')
md.append('- **Total Records:** 180,519 rows')
md.append('- **Total Columns:** 53 columns')
md.append('- **Encoding:** Latin-1 (`latin1`)')
md.append('- **Dataset Granularity:** **Order Item Level** (`Order Item Id` is a unique primary key for every row)')
md.append('- **Parent Entity Grain:** **Order Level** (`Order Id`, 65,752 unique orders, average ~2.75 items per order)\n')

md.append('## 2. Table Column Specifications\n')
md.append('| # | Column Name | Data Type | Non-Null Count | Null % | Unique Values | Sample Value | Description & Business Meaning |')
md.append('|---|---|---|---|---|---|---|---|')

for i, s in enumerate(stats, 1):
    col = s['column']
    dtype = s['dtype']
    non_null = f"{180519 - s['null_count']:,}"
    null_pct = f"{s['null_pct']} %"
    unique = f"{s['unique_count']:,}"
    sample = str(s['sample']).replace('|', '\\|')
    desc = str(s['description']).replace('|', '\\|')
    md.append(f"| {i} | `{col}` | {dtype} | {non_null} | {null_pct} | {unique} | {sample} | {desc} |")

md.append('\n## 3. Entity Classification and Granularity Breakdown\n')
md.append('The 53 columns represent attributes of multiple business domains combined into a single flat denormalized table:\n')
md.append('1. **Order Entity (Order Grain):** `Order Id`, `order date (DateOrders)`, `Order Status`, `Market`, `Order Region`, `Order Country`, `Order State`, `Order City`, `Order Zipcode`, `Order Customer Id`, `Type` (payment type: DEBIT, TRANSFER, PAYMENT, CASH).')
md.append('2. **Order Item Entity (Fact Grain):** `Order Item Id`, `Order Item Cardprod Id`, `Order Item Product Price`, `Order Item Quantity`, `Order Item Discount`, `Order Item Discount Rate`, `Order Item Total` (net revenue), `Sales` (gross revenue), `Order Profit Per Order` (profit contribution per line item), `Order Item Profit Ratio`.')
md.append('3. **Customer Entity:** `Customer Id`, `Customer Fname`, `Customer Lname`, `Customer Segment` (Consumer, Corporate, Home Office), `Customer City`, `Customer State`, `Customer Country`, `Customer Street`, `Customer Zipcode`.')
md.append('4. **Product & Catalog Entity:** `Product Card Id`, `Product Category Id`, `Category Id`, `Category Name`, `Department Id`, `Department Name`, `Product Name`, `Product Price`, `Product Status`, `Product Description` (100% null), `Product Image`.')
md.append('5. **Shipping & Delivery Entity:** `Shipping Mode` (Standard Class, Second Class, First Class, Same Day), `shipping date (DateOrders)`, `Days for shipping (real)`, `Days for shipment (scheduled)`, `Delivery Status` (Late delivery, Advance shipping, Shipping on time, Shipping canceled), `Late_delivery_risk` (binary flag: 1 if late, 0 otherwise).')
md.append('6. **Store / Origin Geography:** `Latitude`, `Longitude`, `Customer State`, `Customer City` (representing store transaction origins).\n')

md.append('## 4. Key Relationships and Integrity Constraints\n')
md.append('- **Primary Fact Key:** `Order Item Id` (180,519 unique values, 0 nulls, 0 duplicates).')
md.append('- **Parent Foreign Key:** `Order Id` (65,752 unique orders).')
md.append('- **Customer Foreign Key:** `Customer Id` / `Order Customer Id` (20,652 unique customers).')
md.append('- **Product Foreign Key:** `Product Card Id` / `Order Item Cardprod Id` (118 unique catalog products).')
md.append('- **Category Foreign Key:** `Category Id` / `Product Category Id` (51 unique categories).')
md.append('- **Department Foreign Key:** `Department Id` (11 unique departments).\n')

out_path = r'D:\Downloads\supply-chain-analytics\docs\data_dictionary.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))

print(f'data_dictionary.md written successfully to {out_path}')
