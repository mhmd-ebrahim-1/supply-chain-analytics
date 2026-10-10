"""
analysis.py
===========
Computes end-to-end exploratory data analysis metrics, cross-tabulations,
and exports high-resolution publication charts to reports/figures/.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

CLEAN_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "supply_chain_clean.csv"))
FIGURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "figures"))
os.makedirs(FIGURES_DIR, exist_ok=True)

def load_data():
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=['order_date', 'shipping_date'])
    df['order_year_month'] = df['order_date'].dt.strftime('%Y-%m')
    return df

def generate_monthly_trends(df):
    print("Generating monthly sales & profit trend chart...")
    monthly = df.groupby('order_year_month').agg(
        net_sales=('net_sales', 'sum'),
        profit=('profit', 'sum'),
        order_count=('order_id', 'nunique'),
        item_count=('order_item_id', 'count')
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax2 = ax1.twinx()

    x = range(len(monthly))
    ax1.plot(x, monthly['net_sales'] / 1e6, color='#1f77b4', marker='o', linewidth=2.2, label='Net Sales ($M)')
    ax2.plot(x, monthly['profit'] / 1e6, color='#2ca02c', marker='s', linewidth=2.0, linestyle='--', label='Profit ($M)')

    ax1.set_title('Monthly Net Sales and Profit Trends (2015 - 2018)', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('Order Year-Month', fontsize=11)
    ax1.set_ylabel('Net Sales ($ Millions)', color='#1f77b4', fontsize=11)
    ax2.set_ylabel('Profit ($ Millions)', color='#2ca02c', fontsize=11)
    ax1.set_xticks(x[::2])
    ax1.set_xticklabels(monthly['order_year_month'].iloc[::2], rotation=45, ha='right')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True)

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, '01_monthly_sales_profit_trend.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved: {out_path}")
    return monthly

def generate_delivery_distribution(df):
    print("Generating delivery performance and delay distribution charts...")
    # Filter to eligible completed shipments
    eligible = df[df['is_eligible_shipment'] == 1].copy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 1. Delivery Status Proportions
    status_counts = df['delivery_status'].value_counts()
    colors = ['#d62728', '#2ca02c', '#1f77b4', '#7f7f7f']
    ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140,
            colors=colors, wedgeprops=dict(width=0.45, edgecolor='w'))
    ax1.set_title('Delivery Status Breakdown (All Transactions)', fontsize=13, fontweight='bold')

    # 2. Delay Days Distribution
    delay_dist = eligible['delay_days'].value_counts().sort_index()
    bar_colors = ['#2ca02c' if x <= 0 else '#d62728' for x in delay_dist.index]
    ax2.bar(delay_dist.index, delay_dist.values, color=bar_colors, edgecolor='#444444', width=0.6)
    ax2.axvline(0, color='black', linestyle=':', linewidth=1.5, label='On-Time Threshold (0 Days)')
    ax2.set_title('Delay Distribution: Real vs Scheduled Days (Eligible Shipments)', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Delay Days (Actual - Scheduled)', fontsize=11)
    ax2.set_ylabel('Shipment Item Count', fontsize=11)
    ax2.set_xticks(delay_dist.index)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, '02_delivery_status_and_delay_distribution.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

def generate_shipping_mode_comparison(df):
    print("Generating shipping mode comparison chart...")
    eligible = df[df['is_eligible_shipment'] == 1].copy()
    mode_stats = eligible.groupby('shipping_mode').agg(
        total_items=('order_item_id', 'count'),
        late_items=('is_late_delivery', 'sum'),
        avg_real_days=('shipping_days_real', 'mean'),
        avg_scheduled_days=('shipping_days_scheduled', 'mean')
    ).reset_index()
    mode_stats['late_rate'] = (mode_stats['late_items'] / mode_stats['total_items']) * 100

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    x = np.arange(len(mode_stats))
    width = 0.35

    rects1 = ax1.bar(x - width/2, mode_stats['avg_real_days'], width, label='Avg Actual Shipping Days', color='#1f77b4')
    rects2 = ax1.bar(x + width/2, mode_stats['avg_scheduled_days'], width, label='Avg Scheduled Shipping Days', color='#aec7e8')
    
    line = ax2.plot(x, mode_stats['late_rate'], color='#d62728', marker='D', linewidth=2.5, label='Late Delivery Rate (%)')

    ax1.set_ylabel('Shipping Days', fontsize=11)
    ax2.set_ylabel('Late Delivery Rate (%)', color='#d62728', fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(mode_stats['shipping_mode'], fontsize=11)
    ax1.set_title('Shipping Mode Transit Comparison: Actual vs Scheduled Duration', fontsize=13, fontweight='bold', pad=15)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, '03_shipping_mode_comparison.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved: {out_path}")
    return mode_stats

def generate_regional_performance(df):
    print("Generating regional performance Pareto chart...")
    eligible = df[df['is_eligible_shipment'] == 1].copy()
    region_stats = eligible.groupby('order_region').agg(
        total_items=('order_item_id', 'count'),
        late_items=('is_late_delivery', 'sum'),
        total_sales=('net_sales', 'sum'),
        total_profit=('profit', 'sum')
    ).reset_index()
    region_stats['late_rate'] = (region_stats['late_items'] / region_stats['total_items']) * 100
    region_stats = region_stats.sort_values(by='late_items', ascending=False)
    region_stats['cum_late_pct'] = (region_stats['late_items'].cumsum() / region_stats['late_items'].sum()) * 100

    top_regions = region_stats.head(12)

    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax2 = ax1.twinx()

    x = range(len(top_regions))
    ax1.bar(x, top_regions['late_items'], color='#ff7f0e', edgecolor='#555555', width=0.6, label='Late Items Count')
    ax2.plot(x, top_regions['cum_late_pct'], color='#1f77b4', marker='o', linewidth=2.2, label='Cumulative Late %')
    ax2.axhline(80, color='gray', linestyle='--', label='80% Pareto Cutoff')

    ax1.set_title('Top 12 Regions: Late Delivery Concentration (Pareto Analysis)', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('Destination Order Region', fontsize=11)
    ax1.set_ylabel('Count of Late Shipments', fontsize=11)
    ax2.set_ylabel('Cumulative % of All Late Shipments', color='#1f77b4', fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(top_regions['order_region'], rotation=40, ha='right')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, '04_regional_late_pareto.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

def generate_product_category_profitability(df):
    print("Generating product & category profitability scatter chart...")
    cat_stats = df.groupby('category_name').agg(
        net_sales=('net_sales', 'sum'),
        profit=('profit', 'sum'),
        item_count=('order_item_id', 'count')
    ).reset_index()
    cat_stats['profit_margin'] = (cat_stats['profit'] / cat_stats['net_sales']) * 100

    fig, ax = plt.subplots(figsize=(12, 7))
    scatter = ax.scatter(
        cat_stats['net_sales'] / 1e6,
        cat_stats['profit'] / 1e6,
        s=cat_stats['item_count'] / 50,
        c=cat_stats['profit_margin'],
        cmap='viridis',
        alpha=0.8,
        edgecolors='black',
        linewidth=0.8
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label('Profit Margin %', fontsize=11)

    # Label top 8 categories
    top_cats = cat_stats.sort_values(by='net_sales', ascending=False).head(8)
    for _, r in top_cats.iterrows():
        ax.annotate(
            r['category_name'],
            (r['net_sales'] / 1e6, r['profit'] / 1e6),
            xytext=(7, 4),
            textcoords='offset points',
            fontsize=9,
            fontweight='semibold'
        )

    ax.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_title('Category Performance: Net Sales vs Profit (Bubble Size = Item Volume)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Total Net Sales ($ Millions)', fontsize=11)
    ax.set_ylabel('Total Profit ($ Millions)', fontsize=11)

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, '05_category_sales_profit_scatter.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

def generate_discount_profit_relationship(df):
    print("Generating discount vs profitability relationship chart...")
    disc_summary = df.groupby('order_item_discount_rate').agg(
        avg_profit=('profit', 'mean'),
        avg_margin=('profit_margin', 'mean'),
        loss_making_pct=('profit', lambda p: (p < 0).mean() * 100),
        item_count=('order_item_id', 'count')
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(11, 6))
    ax2 = ax1.twinx()

    x = disc_summary['order_item_discount_rate'] * 100
    ax1.plot(x, disc_summary['avg_profit'], color='#1f77b4', marker='o', linewidth=2.5, label='Mean Profit per Item ($)')
    ax2.plot(x, disc_summary['loss_making_pct'], color='#d62728', marker='s', linewidth=2.0, linestyle='--', label='% Transactions Unprofitable')

    ax1.axhline(0, color='black', linestyle=':', linewidth=1)
    ax1.set_title('The Impact of Discounting: Margin Erosion & Unprofitable Transactions', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('Order Item Discount Rate (%)', fontsize=11)
    ax1.set_ylabel('Mean Profit per Item ($)', color='#1f77b4', fontsize=11)
    ax2.set_ylabel('% Transactions with Negative Profit', color='#d62728', fontsize=11)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center left')

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, '06_discount_vs_profit_erosion.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    df = load_data()
    generate_monthly_trends(df)
    generate_delivery_distribution(df)
    generate_shipping_mode_comparison(df)
    generate_regional_performance(df)
    generate_product_category_profitability(df)
    generate_discount_profit_relationship(df)
    print("\nAll EDA visualizations successfully produced.")
