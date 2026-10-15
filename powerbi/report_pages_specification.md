# Power BI Dashboard Specification: 4-Page Executive Architecture

Production specification for the Power BI report (`Supply_Chain_Analytics.pbip`) built in PBIR format.

---

## Global Design System & Theme

- **Canvas Standard:** 16:9 (`1280 x 720 px`).
- **Canvas Background:** Cool Light Gray (`#F1F5F9`).
- **Sidebar Panel:** Deep Slate Navy (`#0F172A`) spanning `X: 0, Y: 0, W: 200, H: 720` across all 4 pages:
  - Header branding: `SUPPLY CHAIN BI / Enterprise Analytics`
  - Interactive page navigation: native `pageNavigator`
  - Model summary card: Star Schema 3NF, 180.5K fact rows, 65.7K orders, real-time DAX.
- **Card Styling:** White container (`#FFFFFF`), Soft Gray border (`#E2E8F0`, 8px radius), drop shadow.
- **Top Filter Slicers:** Dropdown style (`mode: 'Dropdown'`), with clean container titles and hidden internal headers.

---

## Page 1: Executive Overview (`page_executive`)

**Purpose:** Enterprise performance tracking across net revenue, operating profit, and volume momentum.

- **Top Slicers:** Fiscal Year (`dim_date[year]`), Market (`dim_geography[market]`), Customer Segment (`dim_customer[customer_segment]`), Order Status (`dim_order[order_status]`).
- **KPI Ribbon (4 Cards):**
  1. `Total Sales` (\$33.05M)
  2. `Total Profit` (\$3.97M)
  3. `Total Orders` (65,752)
  4. `AOV` (\$502.71)
- **Visuals:**
  - **Monthly Sales & Profit Trend:** Line & Clustered Column Combo Chart (`dim_date[year_month]`, Columns: `Total Sales`, Line: `Total Profit`).
  - **Orders by Payment Method:** Clustered Bar Chart (`dim_order[payment_type]`, `Total Orders`).
  - **Net Sales & Profit by Market:** Clustered Bar Chart (`dim_geography[market]`, `Total Sales`, `Total Profit`).
  - **Sales Share by Customer Segment:** Donut Chart (`dim_customer[customer_segment]`, `Total Sales`).

---

## Page 2: Shipping & Logistics - OTIF (`page_shipping`)

**Purpose:** Diagnosis of logistics SLA compliance, transit overruns, and delivery delay distributions.

- **Top Slicers:** Fiscal Year (`dim_date[year]`), Shipping Mode (`dim_shipping[shipping_mode]`), Delivery Status (`dim_shipping[delivery_status]`), Market (`dim_geography[market]`).
- **KPI Ribbon (4 Cards):**
  1. `On-Time Delivery Rate %` (42.7%)
  2. `Late Delivery Rate %` (57.3%)
  3. `Avg Real Shipping Days` (3.50 days)
  4. `Shipping Delay Variance` (+0.57 days)
- **Visuals:**
  - **Scheduled vs. Real Shipping Days by Mode:** Clustered Column Chart (`dim_shipping[shipping_mode]`, Scheduled vs. Real Days).
  - **Orders by Delivery Status & Shipping Mode:** 100% Stacked Bar Chart (`dim_shipping[shipping_mode]`, Legend: `dim_shipping[delivery_status]`).
  - **Late Delivery Risk % Trend:** Area Chart (`dim_date[year_month]`, `Late Delivery Rate %`).
  - **Delivery Performance by Region:** Matrix (`dim_geography[order_region]`, Orders, Late Rate %, Delay Days).

---

## Page 3: Product & Category Performance (`page_product`)

**Purpose:** Catalog SKU profitability, discount sensitivity, and category revenue concentration.

- **Top Slicers:** Fiscal Year (`dim_date[year]`), Department (`dim_product[department_name]`), Category (`dim_product[category_name]`), Market (`dim_geography[market]`).
- **KPI Ribbon (4 Cards):**
  1. `Active Products` (118)
  2. `Total Quantity` (377.6K)
  3. `Profit Margin %` (12.0%)
  4. `Total Discount` (\$5.36M)
- **Visuals:**
  - **Top Product Categories by Sales:** Clustered Bar Chart (`dim_product[category_name]`, `Total Sales`).
  - **Sales Share by Department:** Treemap (`dim_product[department_name]`, `Total Sales`).
  - **Discount vs. Profit Margin by Category:** Scatter Chart (`Avg Discount Rate %` vs. `Profit Margin %`).
  - **Product Performance Details:** Table (`dim_product[product_name]`, Quantity, Sales, Profit, Margin %).

---

## Page 4: Customer & Geo Intelligence (`page_customer`)

**Purpose:** Regional market penetration, customer segment value, and order fulfillment risk.

- **Top Slicers:** Fiscal Year (`dim_date[year]`), Market (`dim_geography[market]`), Order Region (`dim_geography[order_region]`), Customer Segment (`dim_customer[customer_segment]`).
- **KPI Ribbon (4 Cards):**
  1. `Active Customers` (20,652)
  2. `Sales per Customer` (\$1,600.54)
  3. `Countries Reached` (164)
  4. `Suspected Fraud Orders` (4,062)
- **Visuals:**
  - **Global Sales by Order Region:** Clustered Bar Chart (`dim_geography[order_region]`, `Total Sales`).
  - **Orders by Order Status:** Clustered Bar Chart (`dim_order[order_status]`, `Total Orders`).
  - **Top Countries by Sales & Profit:** Line & Clustered Column Combo Chart (`dim_geography[order_country]`, Columns: `Total Sales`, Line: `Total Profit`).
  - **Customer Segment & Country Breakdown:** Matrix (`dim_geography[market]`, Active Customers, Orders, Sales, Profit).
