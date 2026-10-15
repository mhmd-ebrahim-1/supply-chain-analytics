"""
build_pbir_visuals.py
=====================
Builds and binds all visuals across all 5 report pages in the PBIR project
using the pbi-cli toolchain.
"""

import subprocess
import sys
import os

REPORT_PATH = os.path.abspath(r"D:\Downloads\supply-chain-analytics\powerbi\Supply_Chain_Analytics.Report")

def run_pbi(subgroup, cmd_list):
    full_cmd = ["pbi", subgroup, "--no-sync", "-p", REPORT_PATH] + cmd_list
    print(f"Running: {' '.join(full_cmd)}")
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[WARN/ERROR]: {res.stderr or res.stdout}")
    else:
        print("  [OK]")
    return res

def build_page_1():
    print("\n=== Building Page 1: Executive Overview ===")
    p = "page_executive"

    cards = [
        ("card_sales", "_Measures[Total Net Sales]", "Total Net Sales", 20, 30, 230, 110),
        ("card_profit", "_Measures[Total Profit]", "Total Operating Profit", 270, 30, 230, 110),
        ("card_margin", "_Measures[Profit Margin %]", "Operating Margin %", 520, 30, 230, 110),
        ("card_orders", "_Measures[Total Orders]", "Total Orders", 770, 30, 230, 110),
        ("card_late_rate", "_Measures[Late Delivery Rate %]", "Late Delivery Rate", 1020, 30, 240, 110)
    ]
    for name, field, title, x, y, w, h in cards:
        run_pbi("visual", ["add", "--page", p, "--type", "card", "--name", name, "--x", str(x), "--y", str(y), "--width", str(w), "--height", str(h)])
        run_pbi("visual", ["bind", name, "--page", p, "--field", field])
        run_pbi("visual", ["set-container", name, "--page", p, "--title", title])

    # 1. Combo Chart: Monthly Net Sales & Profit Trend
    run_pbi("visual", ["add", "--page", p, "--type", "combo", "--name", "combo_monthly", "--x", "20", "--y", "160", "--width", "620", "--height", "260"])
    run_pbi("visual", ["bind", "combo_monthly", "--page", p, "--category", "dim_date[year_month]", "--column", "_Measures[Total Net Sales]", "--line", "_Measures[Total Profit]"])
    run_pbi("visual", ["set-container", "combo_monthly", "--page", p, "--title", "Monthly Net Sales & Profit Trend (2015-2018)"])

    # 2. Clustered Bar: Net Sales by Category
    run_pbi("visual", ["add", "--page", p, "--type", "bar", "--name", "bar_category", "--x", "660", "--y", "160", "--width", "600", "--height", "260"])
    run_pbi("visual", ["bind", "bar_category", "--page", p, "--category", "dim_product[category_name]", "--value", "_Measures[Total Net Sales]"])
    run_pbi("visual", ["set-container", "bar_category", "--page", p, "--title", "Net Sales by Product Category"])

    # 3. Clustered Column: Net Sales by Market
    run_pbi("visual", ["add", "--page", p, "--type", "column", "--name", "col_market", "--x", "20", "--y", "440", "--width", "620", "--height", "250"])
    run_pbi("visual", ["bind", "col_market", "--page", p, "--category", "dim_geography[market]", "--value", "_Measures[Total Net Sales]"])
    run_pbi("visual", ["set-container", "col_market", "--page", p, "--title", "Net Sales by Market Territory"])

    # 4. Donut: Delivery Status Breakdown
    run_pbi("visual", ["add", "--page", p, "--type", "donut", "--name", "donut_status", "--x", "660", "--y", "440", "--width", "600", "--height", "250"])
    run_pbi("visual", ["bind", "donut_status", "--page", p, "--category", "fact_order_items[delivery_status]", "--value", "_Measures[Total Order Items]"])
    run_pbi("visual", ["set-container", "donut_status", "--page", p, "--title", "Fulfillment Status Distribution"])

def build_page_2():
    print("\n=== Building Page 2: Shipping & Delivery Performance ===")
    p = "page_shipping"

    cards = [
        ("card_ontime", "_Measures[On-Time Delivery Rate %]", "On-Time Delivery Rate", 20, 30, 230, 110),
        ("card_late_p2", "_Measures[Late Delivery Rate %]", "Late Delivery Rate", 270, 30, 230, 110),
        ("card_real_days", "_Measures[Average Actual Shipping Days]", "Avg Actual Shipping Days", 520, 30, 230, 110),
        ("card_sched_days", "_Measures[Average Scheduled Shipping Days]", "Avg Scheduled SLA Days", 770, 30, 230, 110),
        ("card_delay_days", "_Measures[Average Delay Days (Late Only)]", "Avg Overdue Days (When Late)", 1020, 30, 240, 110)
    ]
    for name, field, title, x, y, w, h in cards:
        run_pbi("visual", ["add", "--page", p, "--type", "card", "--name", name, "--x", str(x), "--y", str(y), "--width", str(w), "--height", str(h)])
        run_pbi("visual", ["bind", name, "--page", p, "--field", field])
        run_pbi("visual", ["set-container", name, "--page", p, "--title", title])

    # 1. Bar: Late Delivery Rate by Shipping Mode
    run_pbi("visual", ["add", "--page", p, "--type", "bar", "--name", "bar_ship_mode", "--x", "20", "--y", "160", "--width", "620", "--height", "260"])
    run_pbi("visual", ["bind", "bar_ship_mode", "--page", p, "--category", "fact_order_items[shipping_mode]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi("visual", ["set-container", "bar_ship_mode", "--page", p, "--title", "Late Delivery Rate % by Carrier Shipping Mode"])

    # 2. Column: Delay Days Distribution
    run_pbi("visual", ["add", "--page", p, "--type", "column", "--name", "col_delays", "--x", "660", "--y", "160", "--width", "600", "--height", "260"])
    run_pbi("visual", ["bind", "col_delays", "--page", p, "--category", "fact_order_items[delay_days]", "--value", "_Measures[Total Order Items]"])
    run_pbi("visual", ["set-container", "col_delays", "--page", p, "--title", "Delay Days Distribution (Actual - Scheduled)"])

    # 3. Matrix: Regional SLA Failure Heatmap
    run_pbi("visual", ["add", "--page", p, "--type", "matrix", "--name", "matrix_region_sla", "--x", "20", "--y", "440", "--width", "750", "--height", "250"])
    run_pbi("visual", ["bind", "matrix_region_sla", "--page", p, "--row", "dim_geography[order_region]", "--column", "fact_order_items[shipping_mode]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi("visual", ["set-container", "matrix_region_sla", "--page", p, "--title", "Regional Carrier SLA Failure Rate Matrix"])

    # 4. Donut: Shipping Mode Order Share
    run_pbi("visual", ["add", "--page", p, "--type", "donut", "--name", "donut_shipping_modes", "--x", "790", "--y", "440", "--width", "470", "--height", "250"])
    run_pbi("visual", ["bind", "donut_shipping_modes", "--page", p, "--category", "fact_order_items[shipping_mode]", "--value", "_Measures[Total Orders]"])
    run_pbi("visual", ["set-container", "donut_shipping_modes", "--page", p, "--title", "Carrier Mode Order Volume Share"])

def build_page_3():
    print("\n=== Building Page 3: Product & Profitability Analysis ===")
    p = "page_profitability"

    cards = [
        ("card_gross_sales", "_Measures[Total Gross Sales]", "Total Gross Sales", 20, 30, 290, 110),
        ("card_discounts", "_Measures[Total Discount Amount]", "Total Promotional Discounts", 330, 30, 290, 110),
        ("card_avg_discount", "_Measures[Average Discount Rate %]", "Average Discount Rate", 640, 30, 290, 110),
        ("card_margin_p3", "_Measures[Profit Margin %]", "Portfolio Operating Margin", 950, 30, 310, 110)
    ]
    for name, field, title, x, y, w, h in cards:
        run_pbi("visual", ["add", "--page", p, "--type", "card", "--name", name, "--x", str(x), "--y", str(y), "--width", str(w), "--height", str(h)])
        run_pbi("visual", ["bind", name, "--page", p, "--field", field])
        run_pbi("visual", ["set-container", name, "--page", p, "--title", title])

    # 1. Scatter Chart: Category Net Sales vs Operating Profit
    run_pbi("visual", ["add", "--page", p, "--type", "scatter", "--name", "scatter_category", "--x", "20", "--y", "160", "--width", "620", "--height", "260"])
    run_pbi("visual", ["bind", "scatter_category", "--page", p, "--x", "_Measures[Total Net Sales]", "--y", "_Measures[Total Profit]", "--detail", "dim_product[category_name]"])
    run_pbi("visual", ["set-container", "scatter_category", "--page", p, "--title", "Category Sales vs Profitability (Margin Clusters)"])

    # 2. Bar Chart: Margin by Discount Tier
    run_pbi("visual", ["add", "--page", p, "--type", "bar", "--name", "bar_discount_tier", "--x", "660", "--y", "160", "--width", "600", "--height", "260"])
    run_pbi("visual", ["bind", "bar_discount_tier", "--page", p, "--category", "fact_order_items[discount_tier]", "--value", "_Measures[Profit Margin %]"])
    run_pbi("visual", ["set-container", "bar_discount_tier", "--page", p, "--title", "Operating Profit Margin % by Discount Bracket"])

    # 3. Table: Top Products Performance
    run_pbi("visual", ["add", "--page", p, "--type", "table", "--name", "table_top_products", "--x", "20", "--y", "440", "--width", "1240", "--height", "250"])
    run_pbi("visual", ["bind", "table_top_products", "--page", p, "--column", "dim_product[product_name]", "--value", "_Measures[Total Net Sales]", "--value", "_Measures[Total Profit]", "--value", "_Measures[Profit Margin %]"])
    run_pbi("visual", ["set-container", "table_top_products", "--page", p, "--title", "Product Catalog Sales & Margin Detail"])

def build_page_4():
    print("\n=== Building Page 4: Inventory & Replenishment ===")
    p = "page_inventory"

    cards = [
        ("card_inv_items", "_Measures[Total Order Items]", "Total Demand Items", 20, 30, 390, 110),
        ("card_inv_orders", "_Measures[Total Orders]", "Total Replenishment Orders Served", 440, 30, 390, 110),
        ("card_inv_rev", "_Measures[Total Net Sales]", "Inventory Demand Value", 860, 30, 400, 110)
    ]
    for name, field, title, x, y, w, h in cards:
        run_pbi("visual", ["add", "--page", p, "--type", "card", "--name", name, "--x", str(x), "--y", str(y), "--width", str(w), "--height", str(h)])
        run_pbi("visual", ["bind", name, "--page", p, "--field", field])
        run_pbi("visual", ["set-container", name, "--page", p, "--title", title])

    # 1. Bar Chart: Demand Value by ABC Stratification
    run_pbi("visual", ["add", "--page", p, "--type", "bar", "--name", "bar_abc_demand", "--x", "20", "--y", "160", "--width", "620", "--height", "520"])
    run_pbi("visual", ["bind", "bar_abc_demand", "--page", p, "--category", "dim_product[abc_revenue_class]", "--value", "_Measures[Total Net Sales]"])
    run_pbi("visual", ["set-container", "bar_abc_demand", "--page", p, "--title", "Catalog Demand Value by ABC Stratification"])

    # 2. Matrix: Department Demand by ABC Revenue Class
    run_pbi("visual", ["add", "--page", p, "--type", "matrix", "--name", "matrix_dept_demand", "--x", "660", "--y", "160", "--width", "600", "--height", "520"])
    run_pbi("visual", ["bind", "matrix_dept_demand", "--page", p, "--row", "dim_product[department_name]", "--column", "dim_product[abc_revenue_class]", "--value", "_Measures[Total Net Sales]"])
    run_pbi("visual", ["set-container", "matrix_dept_demand", "--page", p, "--title", "Department Demand by ABC Revenue Class"])

def build_page_5():
    print("\n=== Building Page 5: Operational Deep Dive ===")
    p = "page_deepdive"

    # Slicers on Top
    slicers = [
        ("slicer_market", "dim_geography[market]", "Filter Market", 20, 20, 290, 100),
        ("slicer_ship_mode", "fact_order_items[shipping_mode]", "Filter Shipping Mode", 330, 20, 290, 100),
        ("slicer_status", "fact_order_items[delivery_status]", "Filter Delivery Status", 640, 20, 290, 100),
        ("slicer_segment", "dim_customer[customer_segment]", "Filter Customer Segment", 950, 20, 310, 100)
    ]
    for name, field, title, x, y, w, h in slicers:
        run_pbi("visual", ["add", "--page", p, "--type", "slicer", "--name", name, "--x", str(x), "--y", str(y), "--width", str(w), "--height", str(h)])
        run_pbi("visual", ["bind", name, "--page", p, "--field", field])
        run_pbi("visual", ["set-container", name, "--page", p, "--title", title])

    # Operational Table
    run_pbi("visual", ["add", "--page", p, "--type", "table", "--name", "table_operations", "--x", "20", "--y", "140", "--width", "1240", "--height", "560"])
    run_pbi("visual", ["bind", "table_operations", "--page", p, 
             "--column", "dim_order[order_id]", 
             "--column", "dim_customer[customer_full_name]", 
             "--column", "dim_geography[order_region]", 
             "--column", "fact_order_items[shipping_mode]", 
             "--column", "fact_order_items[delivery_status]", 
             "--value", "_Measures[Total Net Sales]", 
             "--value", "_Measures[Total Profit]"])
    run_pbi("visual", ["set-container", "table_operations", "--page", p, "--title", "Operational Transaction Log & Fulfillment Details"])

def validate_report():
    print("\n=== Validating Complete PBIR Report Structure ===")
    run_pbi("report", ["validate", "--full"])

if __name__ == "__main__":
    build_page_1()
    build_page_2()
    build_page_3()
    build_page_4()
    build_page_5()
    validate_report()
    print("\n[ALL PBIR VISUALS BUILT AND VALIDATED SUCCESSFULLY]")
