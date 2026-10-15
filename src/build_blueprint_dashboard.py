"""
build_blueprint_dashboard.py
============================
Builds the complete, production-ready 4-page Power BI Dashboard for Supply Chain Analytics.
Applies:
- Exact schema mappings: fact_order_items, dim_date, dim_customer, dim_geography, dim_order, dim_product, dim_shipping
- Exact coordinates (1280x720 canvas, sidebar, header, 4 dropdown slicers, 4 KPI cards, middle & bottom visuals)
- Executive UI/UX Design System: #F1F5F9 canvas, #FFFFFF card backgrounds with 8px radius, #E2E8F0 borders, drop shadows
- Dropdown slicers (Style = Dropdown)
- Data Labels ON, Axis Titles OFF on charts
"""

import os
import json
import subprocess
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_PATH = os.path.join(BASE_DIR, "powerbi", "Supply_Chain_Analytics.Report")
PAGES_DIR = os.path.join(REPORT_PATH, "definition", "pages")

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

def build_pages():
    print("\n=== Step 1: Resetting Pages ===")
    existing_pages = [
        "page_executive", "page_shipping", "page_product", "page_customer",
        "page_profitability", "page_inventory", "page_deepdive", "page_logistics", "page_operations"
    ]
    for p in existing_pages:
        run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "delete-page", p], allow_fail=True)

    pages = [
        ("page_executive", "Executive Overview"),
        ("page_shipping", "Shipping & Logistics"),
        ("page_product", "Product & Category Performance"),
        ("page_customer", "Customer & Geo Intelligence"),
    ]
    for name, title in pages:
        run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "add-page", "--name", name, "--display-name", title, "--width", "1280", "--height", "720"])
        run_pbi(["report", "--no-sync", "-p", REPORT_PATH, "set-background", name, "--color", "#F1F5F9"])

        # Add Sidebar visual
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", name, "--type", "textbox", "--name", "sidebar_nav", "--x", "0", "--y", "0", "--width", "200", "--height", "720"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "sidebar_nav", "--page", name, "--title", "SUPPLY CHAIN BI"])

        # Add Header Textbox
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", name, "--type", "textbox", "--name", "header_title", "--x", "216", "--y", "16", "--width", "360", "--height", "52"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "header_title", "--page", name, "--title", title])

    print("\n=== Step 2: Building Page 1: Executive Overview ===")
    p = "page_executive"
    slicers_p1 = [
        ("slicer_p1_year", "592", "155", "dim_date[year]", "Fiscal Year"),
        ("slicer_p1_market", "759", "155", "dim_geography[market]", "Market"),
        ("slicer_p1_segment", "926", "165", "dim_customer[customer_segment]", "Customer Segment"),
        ("slicer_p1_status", "1103", "161", "dim_order[order_status]", "Order Status"),
    ]
    for name, x, w, field, title in slicers_p1:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "slicer", "--name", name, "--x", x, "--y", "16", "--width", w, "--height", "52"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", p, "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", p, "--title", title])

    cards_p1 = [
        ("card_p1_sales", "216", "_Measures[Total Sales]", "Total Sales"),
        ("card_p1_profit", "482", "_Measures[Total Profit]", "Total Profit"),
        ("card_p1_orders", "748", "_Measures[Total Orders]", "Total Orders"),
        ("card_p1_aov", "1014", "_Measures[AOV]", "Average Order Value (AOV)"),
    ]
    for name, x, field, title in cards_p1:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "card", "--name", name, "--x", x, "--y", "84", "--width", "250", "--height", "105"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", p, "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", p, "--title", title])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "combo", "--name", "combo_p1_trajectory", "--x", "216", "--y", "205", "--width", "680", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "combo_p1_trajectory", "--page", p, "--category", "dim_date[full_date]", "--column", "_Measures[Total Sales]", "--line", "_Measures[Total Profit]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "combo_p1_trajectory", "--page", p, "--title", "Monthly Sales & Profit Trend"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "donut", "--name", "donut_p1_segment", "--x", "912", "--y", "205", "--width", "352", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "donut_p1_segment", "--page", p, "--category", "dim_customer[customer_segment]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "donut_p1_segment", "--page", p, "--title", "Sales Share by Customer Segment"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "bar", "--name", "bar_p1_market", "--x", "216", "--y", "461", "--width", "516", "--height", "243"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p1_market", "--page", p, "--category", "dim_geography[market]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p1_market", "--page", p, "--title", "Net Sales & Profit by Market"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "bar", "--name", "bar_p1_payment", "--x", "748", "--y", "461", "--width", "516", "--height", "243"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p1_payment", "--page", p, "--category", "dim_order[payment_type]", "--value", "_Measures[Total Orders]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p1_payment", "--page", p, "--title", "Orders by Payment Method"])

    print("\n=== Step 3: Building Page 2: Shipping & Logistics ===")
    p = "page_shipping"
    slicers_p2 = [
        ("slicer_p2_year", "592", "155", "dim_date[year]", "Fiscal Year"),
        ("slicer_p2_mode", "759", "155", "dim_shipping[shipping_mode]", "Shipping Mode"),
        ("slicer_p2_status", "926", "165", "dim_shipping[delivery_status]", "Delivery Status"),
        ("slicer_p2_market", "1103", "161", "dim_geography[market]", "Market"),
    ]
    for name, x, w, field, title in slicers_p2:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "slicer", "--name", name, "--x", x, "--y", "16", "--width", w, "--height", "52"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", p, "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", p, "--title", title])

    cards_p2 = [
        ("card_p2_ontime", "216", "_Measures[On-Time Delivery Rate %]", "On-Time Delivery Rate %"),
        ("card_p2_late", "482", "_Measures[Late Delivery Rate %]", "Late Delivery Rate %"),
        ("card_p2_real_days", "748", "_Measures[Avg Real Shipping Days]", "Avg Real Shipping Days"),
        ("card_p2_delay", "1014", "_Measures[Shipping Delay Variance]", "Shipping Delay Variance"),
    ]
    for name, x, field, title in cards_p2:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "card", "--name", name, "--x", x, "--y", "84", "--width", "250", "--height", "105"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", p, "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", p, "--title", title])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "column", "--name", "col_p2_mode_days", "--x", "216", "--y", "205", "--width", "516", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "col_p2_mode_days", "--page", p, "--category", "dim_shipping[shipping_mode]", "--value", "_Measures[Avg Real Shipping Days]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "col_p2_mode_days", "--page", p, "--title", "Scheduled vs. Real Shipping Days by Mode"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "bar", "--name", "bar_p2_status_mode", "--x", "748", "--y", "205", "--width", "516", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p2_status_mode", "--page", p, "--category", "dim_shipping[shipping_mode]", "--value", "_Measures[Total Orders]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p2_status_mode", "--page", p, "--title", "Orders by Delivery Status & Shipping Mode"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "area", "--name", "area_p2_late_trend", "--x", "216", "--y", "461", "--width", "516", "--height", "243"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "area_p2_late_trend", "--page", p, "--category", "dim_date[full_date]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "area_p2_late_trend", "--page", p, "--title", "Late Delivery Risk % Trend Over Time"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "matrix", "--name", "matrix_p2_regional", "--x", "748", "--y", "461", "--width", "516", "--height", "243"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "matrix_p2_regional", "--page", p, "--row", "dim_geography[order_region]", "--value", "_Measures[Total Orders]", "--value", "_Measures[Avg Scheduled Shipping Days]", "--value", "_Measures[Avg Real Shipping Days]", "--value", "_Measures[Late Delivery Rate %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "matrix_p2_regional", "--page", p, "--title", "Delivery Performance by Region"])

    print("\n=== Step 4: Building Page 3: Product & Category Performance ===")
    p = "page_product"
    slicers_p3 = [
        ("slicer_p3_year", "592", "155", "dim_date[year]", "Fiscal Year"),
        ("slicer_p3_dept", "759", "155", "dim_product[department_name]", "Department"),
        ("slicer_p3_cat", "926", "165", "dim_product[category_name]", "Category"),
        ("slicer_p3_market", "1103", "161", "dim_geography[market]", "Market"),
    ]
    for name, x, w, field, title in slicers_p3:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "slicer", "--name", name, "--x", x, "--y", "16", "--width", w, "--height", "52"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", p, "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", p, "--title", title])

    cards_p3 = [
        ("card_p3_active_prod", "216", "_Measures[Active Products]", "Active Products"),
        ("card_p3_quantity", "482", "_Measures[Total Quantity]", "Total Quantity"),
        ("card_p3_margin", "748", "_Measures[Profit Margin %]", "Profit Margin %"),
        ("card_p3_discount", "1014", "_Measures[Total Discount]", "Total Discount"),
    ]
    for name, x, field, title in cards_p3:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "card", "--name", name, "--x", x, "--y", "84", "--width", "250", "--height", "105"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", p, "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", p, "--title", title])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "bar", "--name", "bar_p3_categories", "--x", "216", "--y", "205", "--width", "516", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p3_categories", "--page", p, "--category", "dim_product[category_name]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p3_categories", "--page", p, "--title", "Top Product Categories by Sales"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "treemap", "--name", "tree_p3_dept", "--x", "748", "--y", "205", "--width", "516", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "tree_p3_dept", "--page", p, "--category", "dim_product[department_name]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "tree_p3_dept", "--page", p, "--title", "Sales Share by Department"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "scatter", "--name", "scatter_p3_discount", "--x", "216", "--y", "461", "--width", "516", "--height", "243"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "scatter_p3_discount", "--page", p, "--category", "dim_product[category_name]", "--x", "_Measures[Avg Discount Rate %]", "--y", "_Measures[Profit Margin %]", "--legend", "dim_product[department_name]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "scatter_p3_discount", "--page", p, "--title", "Discount Rate vs. Profit Margin by Category"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "table", "--name", "table_p3_details", "--x", "748", "--y", "461", "--width", "516", "--height", "243"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "table_p3_details", "--page", p, "--column", "dim_product[product_name]", "--column", "dim_product[department_name]", "--value", "_Measures[Total Quantity]", "--value", "_Measures[Total Sales]", "--value", "_Measures[Total Profit]", "--value", "_Measures[Profit Margin %]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "table_p3_details", "--page", p, "--title", "Product Performance Details"])

    print("\n=== Step 5: Building Page 4: Customer & Geo Intelligence ===")
    p = "page_customer"
    slicers_p4 = [
        ("slicer_p4_year", "592", "155", "dim_date[year]", "Fiscal Year"),
        ("slicer_p4_market", "759", "155", "dim_geography[market]", "Market"),
        ("slicer_p4_region", "926", "165", "dim_geography[order_region]", "Order Region"),
        ("slicer_p4_segment", "1103", "161", "dim_customer[customer_segment]", "Customer Segment"),
    ]
    for name, x, w, field, title in slicers_p4:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "slicer", "--name", name, "--x", x, "--y", "16", "--width", w, "--height", "52"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", p, "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", p, "--title", title])

    cards_p4 = [
        ("card_p4_active_cust", "216", "_Measures[Active Customers]", "Active Customers"),
        ("card_p4_sales_per_cust", "482", "_Measures[Sales per Customer]", "Sales per Customer"),
        ("card_p4_countries", "748", "_Measures[Countries Reached]", "Countries Reached"),
        ("card_p4_fraud", "1014", "_Measures[Suspected Fraud Orders]", "Suspected Fraud Orders"),
    ]
    for name, x, field, title in cards_p4:
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "card", "--name", name, "--x", x, "--y", "84", "--width", "250", "--height", "105"])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", name, "--page", p, "--field", field])
        run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", name, "--page", p, "--title", title])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "bar", "--name", "bar_p4_region", "--x", "216", "--y", "205", "--width", "600", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p4_region", "--page", p, "--category", "dim_geography[order_region]", "--value", "_Measures[Total Sales]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p4_region", "--page", p, "--title", "Global Sales by Country & Region"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "bar", "--name", "bar_p4_status", "--x", "832", "--y", "205", "--width", "432", "--height", "240"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "bar_p4_status", "--page", p, "--category", "dim_order[order_status]", "--value", "_Measures[Total Orders]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "bar_p4_status", "--page", p, "--title", "Orders by Order Status"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "combo", "--name", "combo_p4_countries", "--x", "216", "--y", "461", "--width", "516", "--height", "243"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "combo_p4_countries", "--page", p, "--category", "dim_geography[order_country]", "--column", "_Measures[Total Sales]", "--line", "_Measures[Total Profit]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "combo_p4_countries", "--page", p, "--title", "Top Countries by Sales & Profit"])

    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "add", "--page", p, "--type", "matrix", "--name", "matrix_p4_segment", "--x", "748", "--y", "461", "--width", "516", "--height", "243"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "bind", "matrix_p4_segment", "--page", p, "--row", "dim_geography[market]", "--value", "_Measures[Active Customers]", "--value", "_Measures[Total Orders]", "--value", "_Measures[Total Sales]", "--value", "_Measures[Total Profit]"])
    run_pbi(["visual", "--no-sync", "-p", REPORT_PATH, "set-container", "matrix_p4_segment", "--page", p, "--title", "Customer Segment & Country Breakdown"])

def post_process_visual_styling():
    print("\n=== Step 6: Post-Processing PBIR Visual Styling ===")
    for root, dirs, files in os.walk(PAGES_DIR):
        if "visual.json" in files:
            vpath = os.path.join(root, "visual.json")
            with open(vpath, "r", encoding="utf-8") as f:
                v = json.load(f)

            vis = v.get("visual", {})
            vtype = vis.get("visualType", "")
            name = v.get("name", "")

            vco = vis.setdefault("visualContainerObjects", {})

            if name == "sidebar_nav":
                vco["background"] = [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                        "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                    }
                }]
            elif name == "header_title":
                vco["background"] = [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "false"}}}
                    }
                }]
            else:
                vco["background"] = [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
                        "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                    }
                }]
                vco["border"] = [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E2E8F0'"}}}}},
                        "radius": {"expr": {"Literal": {"Value": "8D"}}}
                    }
                }]
                vco["dropShadow"] = [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}}
                    }
                }]

            # Slicer: Dropdown mode
            if vtype == "slicer":
                objs = vis.setdefault("objects", {})
                objs["data"] = [{
                    "properties": {
                        "mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}
                    }
                }]

            # Charts: Data Labels ON, Axis Titles OFF
            chart_types = ["barChart", "columnChart", "lineStackedColumnComboChart", "areaChart", "lineChart", "scatterChart", "donutChart"]
            if vtype in chart_types:
                objs = vis.setdefault("objects", {})
                if vtype != "donutChart":
                    objs["dataLabels"] = [{
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}}
                        }
                    }]
                    objs["categoryAxis"] = [{
                        "properties": {
                            "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}
                        }
                    }]
                    objs["valueAxis"] = [{
                        "properties": {
                            "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}}
                        }
                    }]

            with open(vpath, "w", encoding="utf-8") as f:
                json.dump(v, f, indent=2)

    print("All visuals styled successfully with Dropdown mode, white cards, drop shadow, and data labels.")

def validate():
    print("\n=== Step 7: Validating Full PBIR Report ===")
    res = subprocess.run(["pbi", "report", "validate", "--full"], cwd=REPORT_PATH, capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("[ERROR during validation]:", res.stderr)
        sys.exit(1)
    print("[REPORT VALIDATION PASSED]")

def main():
    build_pages()
    post_process_visual_styling()
    validate()

if __name__ == "__main__":
    main()
