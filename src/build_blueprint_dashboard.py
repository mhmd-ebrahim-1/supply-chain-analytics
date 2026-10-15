"""
Build Exact 4-Page Blueprint Supply Chain Analytics Dashboard
According to Full UI/UX Design & Layout Specification:
- Page 1: Executive Overview
- Page 2: Shipping & Logistics (OTIF)
- Page 3: Product & Category Performance
- Page 4: Customer & Geo Intelligence
Canvas: 1280x720, Background: #F1F5F9, Cards: #FFFFFF with #E2E8F0 border
Left Sidebar: 200x720 #0F172A
"""

import subprocess
import sys

REPORT_PATH = r"D:\Downloads\supply-chain-analytics\powerbi\Supply_Chain_Analytics.Report"

def run_pbi(args, allow_fail=False):
    cmd = ["pbi"] + args
    print(f"Running: {' '.join(cmd)}", flush=True)
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        err = res.stderr.strip() or res.stdout.strip()
        print(f"  [ERROR] {err}", flush=True)
        if not allow_fail and "already exists" not in err:
            sys.exit(1)
    else:
        print("  [OK]", flush=True)
    return res.stdout

def add_sidebar(page_name):
    # Add Sidebar Visual (Textbox with dark Navy #0F172A background)
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", page_name, "--type", "textbox", "--name", "sidebar_nav", "--x", "0", "--y", "0", "--width", "200", "--height", "720"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "sidebar_nav", "--page", page_name, "--title", "SUPPLY CHAIN BI"])

def main():
    print("=== Step 1: Cleaning Up Previous Pages ===")
    all_pages = [
        "page_executive", "page_shipping", "page_profitability",
        "page_inventory", "page_deepdive", "page_logistics", "page_operations",
        "page_product", "page_customer"
    ]
    for p in all_pages:
        run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "delete-page", p], allow_fail=True)

    print("\n=== Step 2: Creating 4 Specification Pages ===")
    pages = [
        ("page_executive", "Executive Overview"),
        ("page_shipping", "Shipping & Logistics"),
        ("page_product", "Product & Category Performance"),
        ("page_customer", "Customer & Geo Intelligence"),
    ]
    for name, title in pages:
        run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "add-page", "--name", name, "--display-name", title, "--width", "1280", "--height", "720"])
        run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "set-background", name, "--color", "#F1F5F9"])
        add_sidebar(name)

    print("\n=== Step 3: Populating Page 1: Executive Overview ===")
    # Top Slicers
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "slicer", "--name", "slicer_p1_year", "--x", "650", "--y", "24", "--width", "140", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p1_year", "--page", "page_executive", "--field", "dim_date[year]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p1_year", "--page", "page_executive", "--title", "Fiscal Year"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "slicer", "--name", "slicer_p1_market", "--x", "800", "--y", "24", "--width", "150", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p1_market", "--page", "page_executive", "--field", "dim_geography[market]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p1_market", "--page", "page_executive", "--title", "Market"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "slicer", "--name", "slicer_p1_segment", "--x", "960", "--y", "24", "--width", "150", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p1_segment", "--page", "page_executive", "--field", "dim_customer[customer_segment]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p1_segment", "--page", "page_executive", "--title", "Customer Segment"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "slicer", "--name", "slicer_p1_status", "--x", "1120", "--y", "24", "--width", "140", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p1_status", "--page", "page_executive", "--field", "dim_order[order_status]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p1_status", "--page", "page_executive", "--title", "Order Status"])

    # 4 KPI Cards
    p1_cards = [
        ("card_p1_sales", 216, "_Measures[Total Sales]", "Total Sales"),
        ("card_p1_profit", 482, "_Measures[Total Profit]", "Total Profit"),
        ("card_p1_orders", 748, "_Measures[Total Orders]", "Total Orders"),
        ("card_p1_aov", 1014, "_Measures[AOV]", "Average Order Value (AOV)"),
    ]
    for name, x, field, title in p1_cards:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "card", "--name", name, "--x", str(x), "--y", "88", "--width", "250", "--height", "105"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", "page_executive", "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", "page_executive", "--title", title])

    # Middle Row: Combo Chart + Donut Chart
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "combo", "--name", "combo_p1_trajectory", "--x", "216", "--y", "209", "--width", "680", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "combo_p1_trajectory", "--page", "page_executive", "--category", "dim_date[year_month]", "--column", "_Measures[Total Sales]", "--line", "_Measures[Total Profit]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "combo_p1_trajectory", "--page", "page_executive", "--title", "Monthly Sales & Profit Trend"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "donut", "--name", "donut_p1_segment", "--x", "912", "--y", "209", "--width", "352", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "donut_p1_segment", "--page", "page_executive", "--category", "dim_customer[customer_segment]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "donut_p1_segment", "--page", "page_executive", "--title", "Sales Share by Customer Segment"])

    # Bottom Row: Bar by Market + Bar by Payment Method
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "bar", "--name", "bar_p1_market", "--x", "216", "--y", "465", "--width", "516", "--height", "239"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p1_market", "--page", "page_executive", "--category", "dim_geography[market]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p1_market", "--page", "page_executive", "--title", "Net Sales by Market"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_executive", "--type", "bar", "--name", "bar_p1_payment", "--x", "748", "--y", "465", "--width", "516", "--height", "239"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p1_payment", "--page", "page_executive", "--category", "dim_order[payment_type]", "--value", "_Measures[Total Orders]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p1_payment", "--page", "page_executive", "--title", "Orders by Payment Method"])

    print("\n=== Step 4: Populating Page 2: Shipping & Logistics ===")
    # Top Slicers
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_shipping", "--type", "slicer", "--name", "slicer_p2_mode", "--x", "800", "--y", "24", "--width", "220", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p2_mode", "--page", "page_shipping", "--field", "fact_order_items[shipping_mode]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p2_mode", "--page", "page_shipping", "--title", "Shipping Mode"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_shipping", "--type", "slicer", "--name", "slicer_p2_market", "--x", "1030", "--y", "24", "--width", "230", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p2_market", "--page", "page_shipping", "--field", "dim_geography[market]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p2_market", "--page", "page_shipping", "--title", "Market"])

    # 4 KPI Cards
    p2_cards = [
        ("card_p2_ontime", 216, "_Measures[On-Time Delivery %]", "On-Time Delivery % (OTIF)"),
        ("card_p2_late", 482, "_Measures[Late Delivery Risk %]", "Late Delivery Risk %"),
        ("card_p2_real_days", 748, "_Measures[Avg Real Shipping Days]", "Avg Real Shipping Days"),
        ("card_p2_delay", 1014, "_Measures[Avg Shipping Delay (Days)]", "Avg Shipping Delay (Days)"),
    ]
    for name, x, field, title in p2_cards:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_shipping", "--type", "card", "--name", name, "--x", str(x), "--y", "88", "--width", "250", "--height", "105"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", "page_shipping", "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", "page_shipping", "--title", title])

    # Middle Row: Bar by Mode + Donut Delivery Status
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_shipping", "--type", "bar", "--name", "bar_p2_mode_sla", "--x", "216", "--y", "209", "--width", "516", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p2_mode_sla", "--page", "page_shipping", "--category", "fact_order_items[shipping_mode]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p2_mode_sla", "--page", "page_shipping", "--title", "Late Delivery Rate % by Shipping Mode"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_shipping", "--type", "donut", "--name", "donut_p2_status", "--x", "748", "--y", "209", "--width", "516", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "donut_p2_status", "--page", "page_shipping", "--category", "fact_order_items[delivery_status]", "--value", "_Measures[Total Orders]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "donut_p2_status", "--page", "page_shipping", "--title", "Delivery Status Breakdown"])

    # Bottom Row: Late Rate Trend Area/Line + Regional Matrix
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_shipping", "--type", "line", "--name", "line_p2_late_trend", "--x", "216", "--y", "465", "--width", "516", "--height", "239"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "line_p2_late_trend", "--page", "page_shipping", "--category", "dim_date[year_month]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "line_p2_late_trend", "--page", "page_shipping", "--title", "Late Delivery Rate Trend Over Time"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_shipping", "--type", "matrix", "--name", "matrix_p2_regional", "--x", "748", "--y", "465", "--width", "516", "--height", "239"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "matrix_p2_regional", "--page", "page_shipping", "--row", "dim_geography[order_region]", "--column", "fact_order_items[shipping_mode]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "matrix_p2_regional", "--page", "page_shipping", "--title", "Regional Logistics SLA Compliance Matrix"])

    print("\n=== Step 5: Populating Page 3: Product & Category Performance ===")
    # Top Slicers
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_product", "--type", "slicer", "--name", "slicer_p3_dept", "--x", "800", "--y", "24", "--width", "220", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p3_dept", "--page", "page_product", "--field", "dim_product[department_name]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p3_dept", "--page", "page_product", "--title", "Department"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_product", "--type", "slicer", "--name", "slicer_p3_tier", "--x", "1030", "--y", "24", "--width", "230", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p3_tier", "--page", "page_product", "--field", "fact_order_items[discount_tier]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p3_tier", "--page", "page_product", "--title", "Discount Tier"])

    # 4 KPI Cards
    p3_cards = [
        ("card_p3_prod_sold", 216, "_Measures[Total Products Sold]", "Total Products Sold"),
        ("card_p3_units_sold", 482, "_Measures[Total Units Sold]", "Total Units Sold"),
        ("card_p3_discount", 748, "_Measures[Total Discount Given]", "Total Discount Given"),
        ("card_p3_avg_price", 1014, "_Measures[Avg Product Price]", "Avg Product Catalog Price"),
    ]
    for name, x, field, title in p3_cards:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_product", "--type", "card", "--name", name, "--x", str(x), "--y", "88", "--width", "250", "--height", "105"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", "page_product", "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", "page_product", "--title", title])

    # Middle Row: Categories Bar + Department Treemap
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_product", "--type", "bar", "--name", "bar_p3_categories", "--x", "216", "--y", "209", "--width", "516", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p3_categories", "--page", "page_product", "--category", "dim_product[category_name]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p3_categories", "--page", "page_product", "--title", "Sales by Product Category"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_product", "--type", "treemap", "--name", "tree_p3_dept", "--x", "748", "--y", "209", "--width", "516", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "tree_p3_dept", "--page", "page_product", "--category", "dim_product[department_name]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "tree_p3_dept", "--page", "page_product", "--title", "Sales Share by Department"])

    # Bottom Row: Margin by Discount Bracket + Product Scorecard Table
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_product", "--type", "bar", "--name", "bar_p3_discount_margin", "--x", "216", "--y", "465", "--width", "516", "--height", "239"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p3_discount_margin", "--page", "page_product", "--category", "fact_order_items[discount_tier]", "--value", "_Measures[Profit Margin %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p3_discount_margin", "--page", "page_product", "--title", "Profit Margin % by Discount Bracket"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_product", "--type", "table", "--name", "table_p3_scorecard", "--x", "748", "--y", "465", "--width", "516", "--height", "239"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "table_p3_scorecard", "--page", "page_product", "--column", "dim_product[product_name]", "--column", "dim_product[category_name]", "--value", "_Measures[Total Units Sold]", "--value", "_Measures[Total Sales]", "--value", "_Measures[Total Profit]", "--value", "_Measures[Profit Margin %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "table_p3_scorecard", "--page", "page_product", "--title", "Product Financial Scorecard"])

    print("\n=== Step 6: Populating Page 4: Customer & Geo Intelligence ===")
    # Top Slicers
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_customer", "--type", "slicer", "--name", "slicer_p4_market", "--x", "800", "--y", "24", "--width", "220", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p4_market", "--page", "page_customer", "--field", "dim_geography[market]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p4_market", "--page", "page_customer", "--title", "Market"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_customer", "--type", "slicer", "--name", "slicer_p4_segment", "--x", "1030", "--y", "24", "--width", "230", "--height", "45"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "slicer_p4_segment", "--page", "page_customer", "--field", "dim_customer[customer_segment]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "slicer_p4_segment", "--page", "page_customer", "--title", "Customer Segment"])

    # 4 KPI Cards
    p4_cards = [
        ("card_p4_customers", 216, "_Measures[Active Customers]", "Active Customers"),
        ("card_p4_sales_cust", 482, "_Measures[Sales per Customer]", "Sales per Customer"),
        ("card_p4_countries", 748, "_Measures[Countries Reached]", "Countries Reached"),
        ("card_p4_fraud", 1014, "_Measures[Suspected Fraud Orders]", "Suspected Fraud Orders"),
    ]
    for name, x, field, title in p4_cards:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_customer", "--type", "card", "--name", name, "--x", str(x), "--y", "88", "--width", "250", "--height", "105"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", "page_customer", "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", "page_customer", "--title", title])

    # Middle Row: Column by Region + Bar by Customer Segment
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_customer", "--type", "column", "--name", "col_p4_region", "--x", "216", "--y", "209", "--width", "600", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "col_p4_region", "--page", "page_customer", "--category", "dim_geography[order_region]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "col_p4_region", "--page", "page_customer", "--title", "Geographic Sales Distribution by Region"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_customer", "--type", "bar", "--name", "bar_p4_segment", "--x", "832", "--y", "209", "--width", "432", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p4_segment", "--page", "page_customer", "--category", "dim_customer[customer_segment]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p4_segment", "--page", "page_customer", "--title", "Revenue by Customer Segment"])

    # Bottom Row: Top Customers Table + Order Status & Fraud Risk Bar
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_customer", "--type", "table", "--name", "table_p4_customers", "--x", "216", "--y", "465", "--width", "516", "--height", "239"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "table_p4_customers", "--page", "page_customer", "--column", "dim_customer[customer_full_name]", "--column", "dim_customer[customer_segment]", "--column", "dim_customer[customer_country]", "--value", "_Measures[Total Orders]", "--value", "_Measures[Total Sales]", "--value", "_Measures[Total Profit]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "table_p4_customers", "--page", "page_customer", "--title", "Top Customers by Revenue & Profit"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", "page_customer", "--type", "bar", "--name", "bar_p4_fraud_status", "--x", "748", "--y", "465", "--width", "516", "--height", "239"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p4_fraud_status", "--page", "page_customer", "--category", "dim_order[order_status]", "--value", "_Measures[Total Orders]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p4_fraud_status", "--page", "page_customer", "--title", "Order Status & Fraud Risk Analysis"])

    print("\n=== Step 7: Validating 4-Page Blueprint Report ===")
    run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "validate", "--full"])
    print("\n[ALL 4 BLUEPRINT PAGES BUILT AND VALIDATED SUCCESSFULLY]")

if __name__ == "__main__":
    main()
