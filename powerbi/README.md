# Power BI Implementation & Reproduction Guide

This directory contains everything required to deploy and interact with the **Enterprise Supply Chain Analytics Dashboard** in Microsoft Power BI Desktop.

---

## 1. Files in this Directory

| File Name | Purpose |
|---|---|
| `powerquery_m_code.m` | Automated Power Query M ingestion queries for loading all star schema tables with pre-configured types. |
| `dax_measures.dax` | Ready-to-paste DAX measure definitions formatted with comments and safe division handling. |
| `report_pages_specification.md` | Detailed UX visual design specifications for all 5 dashboard report pages. |
| `screenshots/` | High-resolution captures and visual representations of the analytical dashboard pages. |

---

## 2. Step-by-Step Power BI Setup Instructions

### Step 1: Open Power BI Desktop
1. Launch Power BI Desktop.
2. In the Home ribbon, click **Get Data** $\rightarrow$ **Text/CSV**.

### Step 2: Load the Star Schema Tables
Load the following pre-processed CSV tables from `data/processed/`:
1. `fact_order_items.csv`
2. `dim_date.csv`
3. `dim_product.csv`
4. `dim_customer.csv`
5. `dim_geography.csv`
6. `dim_order.csv`

*(Alternatively, open the Advanced Editor in Power Query and paste the queries from `powerquery_m_code.m`).*

### Step 3: Establish Star Schema Model Relationships
Navigate to the **Model View** and verify the following 1-to-Many relationships:
- `dim_date[date_key]` (1) $\rightarrow$ `fact_order_items[order_date_key]` (*) [Active]
- `dim_date[date_key]` (1) $\rightarrow$ `fact_order_items[shipping_date_key]` (*) [Inactive]
- `dim_product[product_id]` (1) $\rightarrow$ `fact_order_items[product_id]` (*) [Active]
- `dim_customer[customer_id]` (1) $\rightarrow$ `fact_order_items[customer_id]` (*) [Active]
- `dim_geography[geography_id]` (1) $\rightarrow$ `fact_order_items[geography_id]` (*) [Active]
- `dim_order[order_id]` (1) $\rightarrow$ `fact_order_items[order_id]` (*) [Active]

*Ensure Cross filter direction is set to **Single**.*

### Step 4: Add DAX Measures
1. Create a dedicated measure table: Home ribbon $\rightarrow$ **Enter Data** $\rightarrow$ Name table `_Measures`.
2. Right-click `_Measures` $\rightarrow$ **New Measure**, and copy each measure formula from `dax_measures.dax`.

### Step 5: Verify Model Totals
Drag a Card visual onto Page 1 to verify benchmark totals match:
- `[Total Net Sales]` = **\$33,054,402.04**
- `[Total Profit]` = **\$3,966,907.39**
- `[Total Orders]` = **65,752**
- `[Late Delivery Rate %]` = **57.29%**
