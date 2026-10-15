"""
Redesign Power BI Dashboard: Executive, High-Density, Professional Layout
Consolidates 5 sparse pages into 3 comprehensive, beautifully structured pages:
1. Executive Overview & Strategic Health
2. Logistics & Delivery Bottlenecks
3. Commercial Profitability & Operational Deep Dive
"""

import subprocess
import sys
import os
import shutil

REPORT_PATH = r"D:\Downloads\supply-chain-analytics\powerbi\Supply_Chain_Analytics.Report"

def run_pbi(args, allow_fail=False):
    cmd = ["pbi"] + args
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        err = res.stderr.strip() or res.stdout.strip()
        print(f"  [ERROR] {err}")
        if not allow_fail and "already exists" not in err:
            sys.exit(1)
    else:
        print("  [OK]")
    return res.stdout

def main():
    print("=== Step 1: Cleaning Up Old Pages ===")
    all_possible_pages = [
        "page_executive", "page_shipping", "page_profitability",
        "page_inventory", "page_deepdive", "page_logistics", "page_operations"
    ]
    for page in all_possible_pages:
        run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "delete-page", page], allow_fail=True)

    print("\n=== Step 2: Creating 3 Consolidated Executive Pages ===")
    # 1. Executive Command Center
    run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "add-page", "--name", "page_executive", "--display-name", "Executive Overview", "--width", "1280", "--height", "720"])
    run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "set-background", "page_executive", "--color", "#F8FAFC"])

    # 2. Logistics & Delivery Performance
    run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "add-page", "--name", "page_logistics", "--display-name", "Logistics & Delivery Performance", "--width", "1280", "--height", "720"])
    run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "set-background", "page_logistics", "--color", "#F8FAFC"])

    # 3. Profitability & Operational Deep Dive
    run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "add-page", "--name", "page_operations", "--display-name", "Profitability & Operations Deep Dive", "--width", "1280", "--height", "720"])
    run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "set-background", "page_operations", "--color", "#F8FAFC"])

    print("\n=== Step 3: Populating Page 1: Executive Overview ===")
    # Row 1: Slicers Ribbon (y = 15, h = 55)
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "slicer", "--name", "slicer_p1_market", "--x", "20", "--y", "15", "--width", "390", "--height", "55"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p1_market", "--page", "page_executive", "--field", "dim_geography[market]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p1_market", "--page", "page_executive", "--title", "Filter Market"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "slicer", "--name", "slicer_p1_ship_mode", "--x", "430", "--y", "15", "--width", "390", "--height", "55"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p1_ship_mode", "--page", "page_executive", "--field", "fact_order_items[shipping_mode]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p1_ship_mode", "--page", "page_executive", "--title", "Filter Shipping Mode"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "slicer", "--name", "slicer_p1_year", "--x", "840", "--y", "15", "--width", "420", "--height", "55"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p1_year", "--page", "page_executive", "--field", "dim_date[year]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p1_year", "--page", "page_executive", "--title", "Filter Fiscal Year"])

    # Row 2: 5 Top KPI Cards (y = 80, h = 95)
    cards_p1 = [
        ("card_p1_sales", 20, "_Measures[Total Net Sales]", "Net Revenue"),
        ("card_p1_profit", 270, "_Measures[Total Profit]", "Operating Profit"),
        ("card_p1_margin", 520, "_Measures[Profit Margin %]", "Operating Margin %"),
        ("card_p1_orders", 770, "_Measures[Total Orders]", "Total Distinct Orders"),
        ("card_p1_late", 1020, "_Measures[Late Delivery Rate %]", "Late Delivery Rate (SLA)"),
    ]
    for name, x, measure, title in cards_p1:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "card", "--name", name, "--x", str(x), "--y", "80", "--width", "240", "--height", "95"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", "page_executive", "--field", measure])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", "page_executive", "--title", title])

    # Row 3: Mid-section (y = 185, h = 250)
    # Combo Chart: Revenue & Profit Trend
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "combo", "--name", "combo_p1_trajectory", "--x", "20", "--y", "185", "--width", "760", "--height", "250"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "combo_p1_trajectory", "--page", "page_executive", "--category", "dim_date[year_month]", "--column", "_Measures[Total Net Sales]", "--line", "_Measures[Total Profit]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "combo_p1_trajectory", "--page", "page_executive", "--title", "Monthly Revenue & Profit Trajectory"])

    # Bar Chart: Category Revenue Breakdown
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "bar", "--name", "bar_p1_category", "--x", "795", "--y", "185", "--width", "465", "--height", "250"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p1_category", "--page", "page_executive", "--category", "dim_product[category_name]", "--value", "_Measures[Total Net Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p1_category", "--page", "page_executive", "--title", "Net Sales by Product Category"])

    # Row 4: Bottom Section (y = 445, h = 255)
    # Column Chart: Market Sales Comparison
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "column", "--name", "col_p1_market", "--x", "20", "--y", "445", "--width", "760", "--height", "255"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "col_p1_market", "--page", "page_executive", "--category", "dim_geography[market]", "--value", "_Measures[Total Net Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "col_p1_market", "--page", "page_executive", "--title", "Net Sales by Global Market"])

    # Donut Chart: Delivery Status Share
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "donut", "--name", "donut_p1_status", "--x", "795", "--y", "445", "--width", "465", "--height", "255"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "donut_p1_status", "--page", "page_executive", "--category", "fact_order_items[delivery_status]", "--value", "_Measures[Total Net Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "donut_p1_status", "--page", "page_executive", "--title", "Fulfillment Status Distribution"])

    print("\n=== Step 4: Populating Page 2: Logistics & Delivery Performance ===")
    # Row 1: 5 SLA KPI Cards (y = 20, h = 100)
    cards_p2 = [
        ("card_p2_ontime", 20, "_Measures[On-Time Delivery Rate %]", "On-Time Delivery Rate %"),
        ("card_p2_late", 270, "_Measures[Late Delivery Rate %]", "Late Delivery Rate %"),
        ("card_p2_real_days", 520, "_Measures[Average Actual Shipping Days]", "Avg Actual Shipping Days"),
        ("card_p2_sched_days", 770, "_Measures[Average Scheduled Shipping Days]", "Avg Scheduled Transit Days"),
        ("card_p2_delay_days", 1020, "_Measures[Average Delay Days (Late Only)]", "Mean Delay Overrun (Days)"),
    ]
    for name, x, measure, title in cards_p2:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_logistics", "--type", "card", "--name", name, "--x", str(x), "--y", "20", "--width", "240", "--height", "100"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", "page_logistics", "--field", measure])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", "page_logistics", "--title", title])

    # Row 2: Mid-section (y = 135, h = 270)
    # Bar Chart: Shipping Mode SLA Breach
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_logistics", "--type", "bar", "--name", "bar_p2_ship_mode", "--x", "20", "--y", "135", "--width", "610", "--height", "270"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p2_ship_mode", "--page", "page_logistics", "--category", "fact_order_items[shipping_mode]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p2_ship_mode", "--page", "page_logistics", "--title", "Late Delivery Rate % by Shipping Mode"])

    # Column Chart: Delay Days Distribution
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_logistics", "--type", "column", "--name", "col_p2_delays", "--x", "650", "--y", "135", "--width", "610", "--height", "270"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "col_p2_delays", "--page", "page_logistics", "--category", "fact_order_items[delay_days]", "--value", "_Measures[Late Deliveries Count]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "col_p2_delays", "--page", "page_logistics", "--title", "Overdue Transit Distribution (Delay Days)"])

    # Row 3: Bottom Section (y = 420, h = 280)
    # Matrix: Regional SLA Breach Matrix
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_logistics", "--type", "matrix", "--name", "matrix_p2_region_sla", "--x", "20", "--y", "420", "--width", "760", "--height", "280"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "matrix_p2_region_sla", "--page", "page_logistics", "--row", "dim_geography[order_region]", "--column", "fact_order_items[shipping_mode]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "matrix_p2_region_sla", "--page", "page_logistics", "--title", "Regional SLA Compliance Matrix (% Late)"])

    # Donut Chart: Volume Share by Shipping Mode
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_logistics", "--type", "donut", "--name", "donut_p2_ship_volume", "--x", "800", "--y", "420", "--width", "460", "--height", "280"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "donut_p2_ship_volume", "--page", "page_logistics", "--category", "fact_order_items[shipping_mode]", "--value", "_Measures[Total Order Items]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "donut_p2_ship_volume", "--page", "page_logistics", "--title", "Shipment Volume Share by Mode"])

    print("\n=== Step 5: Populating Page 3: Profitability & Operations Deep Dive ===")
    # Row 1: Slicers Header (y = 15, h = 55)
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_operations", "--type", "slicer", "--name", "slicer_p3_market", "--x", "20", "--y", "15", "--width", "300", "--height", "55"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p3_market", "--page", "page_operations", "--field", "dim_geography[market]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p3_market", "--page", "page_operations", "--title", "Filter Market"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_operations", "--type", "slicer", "--name", "slicer_p3_ship_mode", "--x", "330", "--y", "15", "--width", "300", "--height", "55"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p3_ship_mode", "--page", "page_operations", "--field", "fact_order_items[shipping_mode]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p3_ship_mode", "--page", "page_operations", "--title", "Filter Shipping Mode"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_operations", "--type", "slicer", "--name", "slicer_p3_status", "--x", "640", "--y", "15", "--width", "300", "--height", "55"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p3_status", "--page", "page_operations", "--field", "fact_order_items[delivery_status]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p3_status", "--page", "page_operations", "--title", "Filter Delivery Status"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_operations", "--type", "slicer", "--name", "slicer_p3_tier", "--x", "950", "--y", "15", "--width", "310", "--height", "55"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p3_tier", "--page", "page_operations", "--field", "fact_order_items[discount_tier]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p3_tier", "--page", "page_operations", "--title", "Filter Discount Tier"])

    # Row 2: 4 Commercial KPI Cards (y = 80, h = 85)
    cards_p3 = [
        ("card_p3_gross", 20, 302, "_Measures[Total Gross Sales]", "Gross Catalog Sales"),
        ("card_p3_discounts", 332, 302, "_Measures[Total Discounts]", "Total Promotional Discounts"),
        ("card_p3_avg_disc", 644, 302, "_Measures[Average Discount Rate %]", "Average Discount Rate %"),
        ("card_p3_margin", 956, 304, "_Measures[Profit Margin %]", "Realized Operating Margin %"),
    ]
    for name, x, w, measure, title in cards_p3:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_operations", "--type", "card", "--name", name, "--x", str(x), "--y", "80", "--width", str(w), "--height", "85"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", "page_operations", "--field", measure])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", "page_operations", "--title", title])

    # Row 3: Middle Section (y = 175, h = 235)
    # Margin Erosion by Discount Tier
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_operations", "--type", "bar", "--name", "bar_p3_discount_tier", "--x", "20", "--y", "175", "--width", "610", "--height", "235"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p3_discount_tier", "--page", "page_operations", "--category", "fact_order_items[discount_tier]", "--value", "_Measures[Profit Margin %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p3_discount_tier", "--page", "page_operations", "--title", "Operating Profit Margin % by Discount Bracket"])

    # ABC Demand Classification Bar
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_operations", "--type", "bar", "--name", "bar_p3_abc_demand", "--x", "650", "--y", "175", "--width", "610", "--height", "235"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p3_abc_demand", "--page", "page_operations", "--category", "dim_product[abc_revenue_class]", "--value", "_Measures[Total Net Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p3_abc_demand", "--page", "page_operations", "--title", "Catalog Demand Value by ABC Stratification"])

    # Row 4: Transaction & Exception Audit Log (y = 420, h = 285)
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_operations", "--type", "table", "--name", "table_p3_audit", "--x", "20", "--y", "420", "--width", "1240", "--height", "285"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "table_p3_audit", "--page", "page_operations", "--column", "dim_order[order_id]", "--column", "dim_product[product_name]", "--column", "dim_customer[customer_full_name]", "--column", "dim_geography[order_region]", "--column", "fact_order_items[shipping_mode]", "--column", "fact_order_items[delivery_status]", "--value", "_Measures[Total Net Sales]", "--value", "_Measures[Total Profit]", "--value", "_Measures[Profit Margin %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "table_p3_audit", "--page", "page_operations", "--title", "Operational Fulfillment & Commercial Audit Log"])

    print("\n=== Step 6: Validating Complete Redesigned Report ===")
    run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "validate", "--full"])
    print("\n[REDESIGN COMPLETE AND VALIDATED]")

if __name__ == "__main__":
    main()
