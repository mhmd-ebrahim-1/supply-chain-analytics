# Power BI Dashboard Specification: 5-Page Multi-Tier Architecture

This specification defines the visual hierarchy, grid layout, visual cards, charts, slicers, and interactions for the enterprise Supply Chain Analytics report in Power BI Desktop.

---

## Global Design System & Layout Standards

- **Canvas Size:** 16:9 Standard (`1280 x 720` or `1920 x 1080`).
- **Color Palette:**
  - Executive Navy: `#1B365D` (Headers & Primary accents)
  - Neutral Gray: `#F4F6F9` (Canvas Background)
  - Success Green: `#2CA02C` (On-time fulfillments)
  - Alert Red: `#D62728` (Late shipments & losses)
  - Neutral Slate: `#5A6B82` (Secondary labels & text)
- **Top Filter Banner (Synchronized across Pages 1-3 & 5):**
  - Date Range Slicer (`dim_date[year_month]`)
  - Market Slicer (`dim_geography[market]`)
  - Shipping Mode Slicer (`fact_order_items[shipping_mode]`)
  - Customer Segment Slicer (`dim_customer[customer_segment]`)

---

## Page 1: Executive Overview

**Target Audience:** Chief Supply Chain Officer, Chief Executive Officer, VP Operations.  
**Purpose:** Provide a single-pane-of-glass executive diagnosis of corporate revenue, profitability, order volume, and logistics health.

### 1. KPI Metric Banner (Top Horizontal Ribbon)
- **Card 1:** `Total Net Sales` (\$33.06M) with subtitle "Realized Revenue".
- **Card 2:** `Total Profit` (\$3.97M) with conditional font color (>0 green).
- **Card 3:** `Profit Margin %` (12.00%).
- **Card 4:** `Total Orders` (65,752 distinct orders).
- **Card 5:** `Late Delivery Rate %` (57.29% eligible / 54.83% network).

### 2. Primary Visuals (Middle & Lower Grid)
- **Visual 1 (Top Left):** Line & Clustered Column Chart
  - X-Axis: `dim_date[year_month]`
  - Column Y-Axis: `[Total Net Sales]`
  - Line Y-Axis: `[Total Profit]`
  - Analytical Purpose: Tracks monthly macro financial momentum and profitability seasonality.
- **Visual 2 (Top Right):** Clustered Bar Chart
  - Y-Axis: `dim_product[category_name]` (Top 10)
  - X-Axis: `[Total Net Sales]` and `[Total Profit]`
  - Analytical Purpose: Highlights revenue contribution vs profit generation by category.
- **Visual 3 (Bottom Left):** Filled Map / Shape Map or Treemap
  - Location: `dim_geography[market]` & `dim_geography[order_region]`
  - Values: `[Total Net Sales]`, Tooltip: `[Late Delivery Rate %]`, `[Total Profit]`
  - Analytical Purpose: Geographic distribution of sales volume and delivery risk.
- **Visual 4 (Bottom Right):** Donut Chart
  - Legend: `fact_order_items[delivery_status]`
  - Values: `[Total Order Items]`
  - Colors: Late delivery (Red), Shipping on time (Green), Advance shipping (Blue), Shipping canceled (Gray).

---

## Page 2: Shipping & Delivery Performance

**Target Audience:** Director of Logistics, Global Carrier Managers.  
**Purpose:** Granular diagnosis of carrier SLA compliance, transit overruns, and delivery delay distributions.

### 1. Delivery KPI Strip
- **Card 1:** `[On-Time Delivery Rate %]` (42.71%).
- **Card 2:** `[Late Delivery Rate %]` (57.29%).
- **Card 3:** `[Average Actual Shipping Days]` (3.50 days).
- **Card 4:** `[Average Scheduled Shipping Days]` (2.93 days).
- **Card 5:** `[Average Delay Days (Late Only)]` (1.71 days overdue).

### 2. Analytical Visuals
- **Visual 1:** Clustered Bar Chart: Actual vs Scheduled Shipping Days by Shipping Mode
  - Y-Axis: `fact_order_items[shipping_mode]`
  - Values: `[Average Actual Shipping Days]`, `[Average Scheduled Shipping Days]`
  - Line: `[Late Delivery Rate %]`
- **Visual 2:** Column Chart: Delay Days Distribution
  - X-Axis: `fact_order_items[delay_days]` (-2, -1, 0, 1, 2, 3, 4)
  - Y-Axis: `[Total Order Items]`
  - Conditional Formatting: $\le 0$ Green, $>0$ Red.
- **Visual 3:** Matrix Visual: Regional Carrier Performance Heatmap
  - Rows: `dim_geography[order_region]`
  - Columns: `fact_order_items[shipping_mode]`
  - Values: `[Late Delivery Rate %]` (Color scale background from Green at 40% to Dark Red at 70%).
- **Visual 4:** 100% Stacked Bar Chart: Delivery Status by Category
  - Y-Axis: `dim_product[category_name]`
  - X-Axis: `% Share of Delivery Status`

---

## Page 3: Product & Profitability Analysis

**Target Audience:** VP Merchandising, Pricing Analysts, Category Managers.  
**Purpose:** Uncover unprofitable products, evaluate discount margin destruction, and identify catalog rationalization candidates.

### 1. Commercial KPI Cards
- **Card 1:** `[Total Gross Sales]` (\$35.78M).
- **Card 2:** `[Total Discount Amount]` (\$2.72M).
- **Card 3:** `[Average Discount Rate %]` (10.15%).
- **Card 4:** `% Loss-Making Lines` (24.21% of lines sold at a loss).

### 2. Analytical Visuals
- **Visual 1:** Scatter Plot: Category Sales vs Profitability
  - X-Axis: `[Total Net Sales]`
  - Y-Axis: `[Total Profit]`
  - Bubble Size: `[Total Order Items]`
  - Details: `dim_product[category_name]`
- **Visual 2:** Line Chart: Discount Rate vs Unit Profitability Inflection Point
  - X-Axis: `fact_order_items[discount_tier]` (0%, 1-10%, 11-18%, >18%)
  - Y-Axis: `Average Profit per Item` and `% Transactions with Negative Profit`
- **Visual 3:** Table: Top 10 High-Sales Low-Margin Products (Action Candidates)
  - Columns: `Product Name`, `Category`, `Net Sales`, `Profit`, `Margin %`, `Avg Discount Rate`
  - Conditional Formatting: Margin < 8% highlighted in soft red.

---

## Page 4: Inventory & Replenishment (Architecture & Extension Guide)

**Target Audience:** Supply Chain Architects, Inventory Planners.  
**Purpose:** Transparently explain the boundary of transaction-level data vs ERP inventory balances, and provide the conceptual template for multi-echelon replenishment when stock balances are ingested.

### Visual Elements & Architecture Showcase
1. **Notice Callout Banner:**
   - "Primary transaction dataset contains sales demand history but lacks periodic warehouse stock ledger snapshots. Do not impute fictitious stock levels. Below is the production implementation specification for warehouse ERP integration."
2. **Planned Inventory KPIs Card Mockups:**
   - Target KPI 1: `Stock on Hand (Units & Value)`
   - Target KPI 2: `Inventory Turnover Ratio (COGS / Avg Stock)`
   - Target KPI 3: `Days of Inventory Outstanding (DIO)`
   - Target KPI 4: `Stockout Rate (% Demands Unfulfilled)`
   - Target KPI 5: `Dynamic Safety Stock (SS = Z * sqrt(L * sigma_d^2 + d^2 * sigma_L^2))`
3. **Data Pipeline Architecture Diagram:** Displaying the ingestion pipeline required from SAP/Oracle ERP warehouse tables to Power BI.

---

## Page 5: Operational Deep Dive & Line-Item Drill-Through

**Target Audience:** Logistics Dispatchers, Customer Support Leads.  
**Purpose:** Interactive tabular drill-down to inspect specific high-delay orders, carrier performance anomalies, and individual order-item transactions.

### 1. Operational Filter Slicers
- Order ID Search box
- Delivery Status Dropdown
- Delay Days Slider ($\ge 1$)

### 2. Transaction Exception Table Visual
- **Columns:**
  - `Order Id`
  - `Order Date`
  - `Customer Name`
  - `Destination Region`
  - `Product Name`
  - `Shipping Mode`
  - `Scheduled Days`
  - `Actual Days`
  - `Delay Days` (Overdue)
  - `Net Sales`
  - `Profit`
  - `Delivery Status`
- **Conditional Formatting:** Highlighting `Delay Days` $>2$ in bold red text.
