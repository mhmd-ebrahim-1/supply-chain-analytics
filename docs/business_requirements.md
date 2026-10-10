# Business Requirements Document (BRD): Supply Chain & Logistics Analytics

## 1. Project Context & Objectives

A global omnichannel retail enterprise manages shipments across 5 global markets (Europe, LATAM, Pacific Asia, USCA, Africa) utilizing four carrier shipping tiers (Standard Class, Second Class, First Class, Same Day). 

The executive leadership team requires an end-to-end analytical framework to diagnose:
1. Operational delivery bottlenecks and late shipment root causes.
2. Product catalog profitability, margin leakage from excessive discounts, and volume-profit decoupling.
3. Fulfillment performance by regional markets, carriers, and merchant categories.
4. Data requirements and architectural roadmaps for future multi-echelon inventory replenishment.

---

## 2. Core Stakeholders & Analytical Views

| Stakeholder Group | Primary Business Questions | Decision / Action Powered by Analytics |
|---|---|---|
| **Chief Supply Chain Officer (CSCO)** | What is our company-wide on-time delivery rate? Which regions, carriers, and product lines drive fulfillment failures? | Carrier SLA renegotiation, routing reallocations, logistics hub capacity planning. |
| **Director of Logistics & Operations** | Which shipping methods routinely fail scheduled transit times? What is our average transit delay? | Carrier selection optimization, scheduled commitment window calibration. |
| **VP of Merchandising & Commercial** | Which high-volume product categories are destroying margin through aggressive discount structures? | Pricing tier adjustments, discount capping, catalog rationalization. |
| **Regional Fulfillment Managers** | Why are specific destination territories (e.g., Southeast Asia, Western Europe) lagging in delivery timeliness? | Regional carrier partnerships, local 3PL fulfillment routing. |
| **Inventory & Procurement Planners** | What data pipeline extensions are needed to track safety stock and reorder points? | Specification of ERP inventory snapshot integration requirements. |

---

## 3. Core Business Questions & Acceptance Criteria

### BQ-1: Overall Delivery Performance & Late Shipment Rates
- **Question:** What is the macro fulfillment success rate? What percentage of eligible shipments arrive late?
- **Acceptance Criterion:** Compute late rate both across all orders and strictly among delivered shipments (excluding cancellations). Quantify average transit delay days.

### BQ-2: Carrier & Shipping Method Timeliness
- **Question:** How do carrier service levels compare across Standard Class, Second Class, First Class, and Same Day?
- **Acceptance Criterion:** Benchmark scheduled vs actual shipping days, failure rate per class, and order volume concentration.

### BQ-3: Regional & Geographic Disparities
- **Question:** Which markets and regional territories account for the largest share of late shipments?
- **Acceptance Criterion:** Pareto analysis of late deliveries across all 23 order regions and 5 markets.

### BQ-4: Product & Category Profitability vs Sales Volume
- **Question:** Which categories generate the bulk of revenue, and which suffer from margin erosion?
- **Acceptance Criterion:** ABC classification of catalog items by revenue and profit; scatter analysis highlighting high-sales low-margin products.

### BQ-5: Discount-Driven Margin Dilution
- **Question:** What is the relationship between discount rate tiers (0% to 25%) and line-item profitability?
- **Acceptance Criterion:** Cross-tabulation and regression analysis demonstrating the inflection point where discount brackets induce negative operating profits.

### BQ-6: Temporal & Seasonality Dynamics
- **Question:** What are the monthly revenue, order volume, and delivery punctuality trends over time?
- **Acceptance Criterion:** Continuous monthly time-series decomposition from January 2015 through January 2018.

---

## 4. Operational Recommendations Framework

Management actions prioritized by impact:
1. **Calibrate Transit Commitment Algorithms:** Realign promised delivery windows with empirical carrier transit distributions (e.g., First Class and Standard Class consistently overrun 2-day promises).
2. **Institute Discount Ceilings:** Limit sales discount rates below 18% on high COGS items to eliminate loss-making transactions.
3. **Regional Carrier Diversification:** Implement alternative 3PL partnerships in high-delay regions.
4. **Order Item Aggregation Governance:** Ensure BI dashboards consistently calculate order-level KPIs without duplicating line-item records.

---

## 5. Inventory Extension & Missing Data Requirements

As verified during data profiling, the primary dataset contains transaction orders but lacks inventory balance tables. To support an operational inventory module, the following data entities are required:

| Missing Entity | Required Fields | Analytical Capability Unlocked |
|---|---|---|
| **Warehouse Stock Balances** | `warehouse_id`, `product_id`, `on_hand_qty`, `allocated_qty`, `snapshot_date` | Stock on Hand, Stockout Frequency, Days of Inventory (DOI). |
| **Inbound Purchase Orders** | `po_id`, `vendor_id`, `product_id`, `order_date`, `receipt_date`, `qty_ordered`, `qty_received` | Supplier Lead Time Variability, On-Time In-Full (OTIF) vendor rating. |
| **Inventory Carrying Costs** | `product_id`, `holding_cost_pct`, `unit_storage_cost`, `ordering_cost_fixed` | Economic Order Quantity (EOQ), Total Inventory Holding Cost. |
| **Service Level Targets** | `category_id`, `target_fill_rate` (e.g. 95%, 99%), `z_score` | Safety Stock modeling, dynamic Reorder Point (ROP) calculation. |
