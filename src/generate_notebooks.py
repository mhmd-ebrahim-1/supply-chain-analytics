"""
generate_notebooks.py
=====================
Programmatically builds reproducible Jupyter notebooks for the repository.
"""

import json
import os

nb_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "notebooks"))
os.makedirs(nb_dir, exist_ok=True)

def make_nb(cells):
    return {
        'cells': cells,
        'metadata': {
            'language_info': {'name': 'python', 'version': '3.11'},
            'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
        },
        'nbformat': 4,
        'nbformat_minor': 5
    }

def md_cell(source):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': source if isinstance(source, list) else source.splitlines(True)}

def code_cell(source):
    return {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': source if isinstance(source, list) else source.splitlines(True)}

# 01 Data Profiling Notebook
nb1_cells = [
    md_cell("# 01. Data Discovery & Profiling\n## DataCo Smart Supply Chain Dataset\nThis notebook performs initial schema inspection, data type detection, key analysis, missing value auditing, and data quality validation."),
    code_cell("import pandas as pd\nimport numpy as np\nimport os\n\nraw_path = '../data/raw/DataCoSupplyChainDataset.csv'\ndf = pd.read_csv(raw_path, encoding='latin1')\nprint(f'Loaded {len(df):,} rows and {len(df.columns)} columns.')"),
    code_cell("print('--- Dataset Information ---')\ndf.info()"),
    code_cell("print('--- Grain & Entity Key Uniqueness ---')\nprint('Order Item Id unique:', df['Order Item Id'].nunique())\nprint('Order Id unique:', df['Order Id'].nunique())\nprint('Product Card Id unique:', df['Product Card Id'].nunique())\nprint('Customer Id unique:', df['Customer Id'].nunique())"),
    code_cell("print('--- Missing Values Analysis ---')\nnulls = df.isnull().sum()\nnull_report = pd.DataFrame({'null_count': nulls, 'null_pct': (nulls / len(df) * 100).round(2)})\nnull_report[null_report['null_count'] > 0]"),
    code_cell("print('--- Delivery Status Distribution ---')\nprint(df['Delivery Status'].value_counts(dropna=False))"),
    code_cell("print('--- Date Coverage ---')\nprint('Order Date:', df['order date (DateOrders)'].min(), 'to', df['order date (DateOrders)'].max())\nprint('Shipping Date:', df['shipping date (DateOrders)'].min(), 'to', df['shipping date (DateOrders)'].max())")
]
with open(os.path.join(nb_dir, '01_data_profiling.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(make_nb(nb1_cells), f, indent=2)

# 02 Data Cleaning Notebook
nb2_cells = [
    md_cell("# 02. Data Cleaning & Normalization\nThis notebook walks through column renaming, null imputation, type casting, derived metric engineering, and exporting the clean analytical dataset."),
    code_cell("import pandas as pd\nimport numpy as np\nimport sys\nsys.path.append('..')\nfrom src.data_cleaning import load_raw_data, clean_dataset, save_clean_data\nfrom src.data_validation import run_validation_suite"),
    code_cell("raw_df = load_raw_data('../data/raw/DataCoSupplyChainDataset.csv')\ncleaned_df = clean_dataset(raw_df)\ncleaned_df.head()"),
    code_cell("run_validation_suite(cleaned_df)"),
    code_cell("save_clean_data(cleaned_df, '../data/processed')")
]
with open(os.path.join(nb_dir, '02_data_cleaning.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(make_nb(nb2_cells), f, indent=2)

# 03 Exploratory Analysis Notebook
nb3_cells = [
    md_cell("# 03. Exploratory Data Analysis & Strategic Insights\nInvestigates fulfillment bottlenecks, carrier SLA compliance, category profitability, and discount margin erosion."),
    code_cell("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport sys\nsys.path.append('..')\nfrom src.analysis import load_data, generate_monthly_trends, generate_delivery_distribution, generate_shipping_mode_comparison, generate_regional_performance, generate_product_category_profitability, generate_discount_profit_relationship"),
    code_cell("df = pd.read_csv('../data/processed/supply_chain_clean.csv', parse_dates=['order_date', 'shipping_date'])\ndf.head()"),
    code_cell("generate_monthly_trends(df)"),
    code_cell("generate_delivery_distribution(df)"),
    code_cell("generate_shipping_mode_comparison(df)"),
    code_cell("generate_regional_performance(df)"),
    code_cell("generate_product_category_profitability(df)"),
    code_cell("generate_discount_profit_relationship(df)")
]
with open(os.path.join(nb_dir, '03_exploratory_analysis.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(make_nb(nb3_cells), f, indent=2)

print("All 3 notebooks generated successfully in", nb_dir)
