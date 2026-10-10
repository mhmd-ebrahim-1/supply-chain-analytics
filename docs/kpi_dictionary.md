# Enterprise KPI Dictionary: Supply Chain & Logistics Analytics

This dictionary establishes standard metrics, formulas, granularities, and business rules across Python scripts, SQL queries, and Power BI DAX measures.

---

## 1. Summary of Standard Metrics

| KPI Name | Business Domain | Fact Grain | Power BI / SQL Measure Type |
|---|---|---|---|
| **Total Sales (Gross)** | Financial | Order Item | Additive Aggregate (`SUM`) |
| **Total Net Revenue** | Financial | Order Item | Additive Aggregate (`SUM`) |
| **Total Profit** | Financial | Order Item | Additive Aggregate (`SUM`) |
| **Profit Margin %** | Financial | Calculated Ratio | Ratio (`Net Profit / Net Revenue`) |
| **Total Orders** | Operational | Order | Distinct Count (`COUNT(DISTINCT Order Id)`) |
| **Total Order Items** | Operational | Order Item | Row Count (`COUNT(Order Item Id)`) |
| **Average Order Value (AOV)** | Operational | Order | Ratio (`Net Revenue / Total Orders`) |
| **Items Per Order** | Operational | Order | Ratio (`Total Items / Total Orders`) |
| **Eligible Delivered Shipments**| Fulfillment | Order Item | Filtered Count (`Delivery Status != 'Shipping canceled'`) |
| **Late Delivery Rate (Eligible)**| Fulfillment | Order Item | Ratio (`Late Deliveries / Eligible Shipments`) |
| **Late Delivery Rate (Total)** | Fulfillment | Order Item | Ratio (`Late Deliveries / Total Items`) |
| **On-Time Delivery Rate (Eligible)**| Fulfillment | Order Item | Ratio (`(Advance + On-Time) / Eligible Shipments`) |
| **Shipping Cancellation Rate** | Fulfillment | Order Item | Ratio (`Canceled Shipments / Total Items`) |
| **Average Actual Shipping Days**| Logistics | Order Item | Average (`AVG(Days for shipping real)`) |
| **Average Scheduled Shipping Days**| Logistics | Order Item | Average (`AVG(Days for shipment scheduled)`) |
| **Average Delivery Delay Days** | Logistics | Order Item | Filtered Average (`AVG(Days real - Days scheduled)` where delay > 0) |

---

## 2. Detailed Metric Specifications

### KPI-01: Total Net Revenue
- **Business Definition:** Total net revenue billed to customers after accounting for item discounts.
- **Formula:** $\sum (\text{Order Item Total})$
- **Numerator:** Sum of net transaction value.
- **Denominator:** N/A.
- **Data Source & Grain:** `data/raw/DataCoSupplyChainDataset.csv`, grain: **Order Item**.
- **Inclusion / Exclusion Rules:** Include all valid order statuses except `CANCELED` and `SUSPECTED_FRAUD` when evaluating realized cash revenue, or include all records when analyzing gross pipeline intent.
- **Known Limitations:** Does not account for post-delivery customer chargebacks.

---

### KPI-02: Total Profit
- **Business Definition:** Total earnings generated per line item sold.
- **Formula:** $\sum (\text{Order Profit Per Order})$
- **Numerator:** Sum of line-item net margins.
- **Denominator:** N/A.
- **Data Source & Grain:** `Order Profit Per Order` (equivalent to `Benefit per order`), grain: **Order Item**.
- **Inclusion / Exclusion Rules:** Negative values represent transactions where product costs plus discounts exceeded revenue.
- **Known Limitations:** Cost structure is fixed at transaction creation; does not factor in variable shipping overruns.

---

### KPI-03: Profit Margin %
- **Business Definition:** Net profit percentage realized on net revenue.
- **Formula:** $\frac{\text{Total Profit}}{\text{Total Net Revenue}} \times 100\%$
- **Numerator:** $\sum (\text{Order Profit Per Order})$
- **Denominator:** $\sum (\text{Order Item Total})$
- **Data Source & Grain:** Aggregated from Order Item grain.
- **Inclusion / Exclusion Rules:** Handle divide-by-zero by returning 0 or BLANK when denominator is zero.

---

### KPI-04: Total Orders
- **Business Definition:** The count of unique customer orders placed.
- **Formula:** $\text{COUNT}(\text{DISTINCT } \text{Order Id})$
- **Numerator:** Count of distinct order keys.
- **Denominator:** N/A.
- **Data Source & Grain:** Order Level (`Order Id`).
- **Inclusion / Exclusion Rules:** Must NOT use `COUNT(Order Item Id)` or `COUNT(Order Id)` without `DISTINCT`, which would overstate order counts by ~2.75x.

---

### KPI-05: Late Delivery Rate (Eligible / Standard)
- **Business Definition:** The proportion of successfully fulfilled shipments that arrived after the scheduled delivery date.
- **Formula:** 
  $$\text{Late Delivery Rate}_{\text{eligible}} = \frac{\sum [\text{Delivery Status} = \text{'Late delivery'}]}{\sum [\text{Delivery Status} \neq \text{'Shipping canceled'}]}$$
- **Numerator:** Count of order items with `Delivery Status = 'Late delivery'`.
- **Denominator:** Count of order items where `Delivery Status` is in `('Late delivery', 'Advance shipping', 'Shipping on time')`.
- **Data Source & Grain:** `Delivery Status`, `Days for shipping (real)`, `Days for shipment (scheduled)`. Grain: **Order Item**.
- **Inclusion / Exclusion Rules:** Excludes canceled shipments (`Shipping canceled`) because non-delivered items cannot be considered late deliveries.
- **Empirical Baseline:** 98,977 / 172,765 = **57.29%**.

---

### KPI-06: On-Time Delivery Rate (Eligible)
- **Business Definition:** Proportion of fulfilled shipments that arrived on or ahead of schedule.
- **Formula:**
  $$\text{On-Time Delivery Rate} = \frac{\sum [\text{Delivery Status} \in (\text{'Advance shipping'}, \text{'Shipping on time'})]}{\sum [\text{Delivery Status} \neq \text{'Shipping canceled'}]}$$
- **Empirical Baseline:** (41,592 + 32,196) / 172,765 = 73,788 / 172,765 = **42.71%**.
- **Complement:** Equals $1 - \text{Late Delivery Rate}_{\text{eligible}}$.

---

### KPI-07: Average Delivery Delay (Days)
- **Business Definition:** The mean number of days overdue for shipments that experienced transit delays.
- **Formula:**
  $$\text{Avg Delay Days} = \frac{\sum (\text{Days for shipping (real)} - \text{Days for shipment (scheduled)})}{\text{Count of Delayed Shipments}} \quad \text{where } \text{Days real} > \text{Days scheduled}$$
- **Numerator:** Total cumulative delay days.
- **Denominator:** Total count of delayed order items.
- **Empirical Baseline:** Mean delay is **1.71 days** for late shipments (ranging from 1 to 4 days).

---

### KPI-08: Average Actual vs Scheduled Shipping Days
- **Business Definition:** The comparative transit duration between carrier SLA commitment and actual warehouse-to-door delivery.
- **Formula:**
  - $\text{Avg Actual Days} = \text{AVG}(\text{Days for shipping (real)})$
  - $\text{Avg Scheduled Days} = \text{AVG}(\text{Days for shipment (scheduled)})$
- **Empirical Baseline:** Across all 180,519 records, Avg Actual is **3.50 days** vs Avg Scheduled of **2.93 days** (average operational overrun of **+0.57 days** across entire logistics network).
