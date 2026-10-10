# Dataset Documentation & Setup Guide

## 1. Primary Dataset Overview

The dataset used in this project is the **DataCo Smart Supply Chain for Big Data Analysis**, published on Kaggle by Shashwat Shukla:
- **Kaggle Dataset URL:** [DataCo Smart Supply Chain for Big Data Analysis](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **File Format:** CSV (`DataCoSupplyChainDataset.csv`, `DescriptionDataCoSupplyChain.csv`, `tokenized_access_logs.csv`)
- **Encoding:** Latin-1 (`latin1` / `ISO-8859-1` / `cp1252`)
- **Raw File Size:** 95.9 MB
- **Total Records:** 180,519 rows
- **Total Fields:** 53 columns
- **Primary Granularity:** Single Order Item (`Order Item Id` is unique per record)

---

## 2. Dataset Files in `data/raw/`

| File Name | File Size | Description |
| :--- | :--- | :--- |
| `DataCoSupplyChainDataset.csv` | ~95.9 MB | Primary operational transaction dataset containing 180,519 order-item records spanning 2015 to early 2018. |
| `DescriptionDataCoSupplyChain.csv` | ~4.7 KB | Official metadata mapping descriptions for all 53 columns in the primary dataset. |
| `tokenized_access_logs.csv` | ~95.4 MB | Web server clickstream logs containing tokenized user browsing interactions, IP addresses, departments, and URLs. |

---

## 3. How to Obtain and Setup the Dataset

If the dataset is missing or being reproduced from scratch:

### Automated Method (via Kaggle API or Python script)
1. Run the project ingestion pipeline:
   ```bash
   python src/data_ingestion.py
   ```
   This script checks if the raw files exist in `data/raw/`. If not, it pulls the archive directly from Kaggle and extracts it.

### Manual Download Instructions
1. Navigate to [Kaggle Dataset Page](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis).
2. Click **Download (Archive.zip)**.
3. Extract the contents directly into:
   ```
   supply-chain-analytics/data/raw/
   ```
4. Verify the file names match:
   - `DataCoSupplyChainDataset.csv`
   - `DescriptionDataCoSupplyChain.csv`

---

## 4. Ground Truth on Inventory Information

> **Critical Analytical Finding:**
> Inspection of the raw schema and records reveals that **no warehouse inventory balances, periodic stock levels, replenishments, safety stock parameters, or supplier lead times exist in this dataset**.
> The column `Product Status` is present in the schema, but is uniform (`0` for all 180,519 records).
> In accordance with strict data integrity rules, **inventory optimization metrics (EOQ, safety stock, stockout rates, days of inventory) cannot and must not be fabricated from sales transaction records alone**.
> An optional inventory modeling extension with clearly stated parameters and synthetic operational replenishment data is documented separately in `docs/business_requirements.md`.
