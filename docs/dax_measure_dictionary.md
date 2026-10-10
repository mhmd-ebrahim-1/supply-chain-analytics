# Enterprise DAX Measure Dictionary: Supply Chain Analytics

This document contains production-grade DAX measures designed for the Power BI Star Schema semantic model. All measures follow formatting best practices, safe division handling (`DIVIDE`), and explicit filter context management.

---

## 1. Core Financial Measures

### [Total Gross Sales]
```dax
Total Gross Sales = 
SUM(fact_order_items[gross_sales])
```
- **Description:** Sum of gross line-item sales prior to promotional discounts.
- **Format:** Currency (`$#,##0.00`)

### [Total Net Sales]
```dax
Total Net Sales = 
SUM(fact_order_items[net_sales])
```
- **Description:** Sum of realized net sales collected from customers.
- **Format:** Currency (`$#,##0.00`)

### [Total Profit]
```dax
Total Profit = 
SUM(fact_order_items[profit])
```
- **Description:** Cumulative operating profit contribution across all fulfilled items.
- **Format:** Currency (`$#,##0.00`)

### [Profit Margin %]
```dax
Profit Margin % = 
DIVIDE(
    [Total Profit],
    [Total Net Sales],
    BLANK()
)
```
- **Description:** Realized profit percentage. Safely returns BLANK if net sales are zero.
- **Format:** Percentage (`0.00%`)

### [Total Discount Amount]
```dax
Total Discount Amount = 
SUM(fact_order_items[order_item_discount])
```
- **Description:** Total dollar value granted to customers in price reductions.
- **Format:** Currency (`$#,##0.00`)

### [Average Discount Rate %]
```dax
Average Discount Rate % = 
AVERAGE(fact_order_items[order_item_discount_rate])
```
- **Description:** Unweighted mean discount percentage applied to transaction lines.
- **Format:** Percentage (`0.00%`)

---

## 2. Order Volume & Operational Metrics

### [Total Orders]
```dax
Total Orders = 
DISTINCTCOUNT(fact_order_items[order_id])
```
- **Description:** Distinct count of customer order headers. Prevents double-counting from multi-line orders.
- **Format:** Whole Number (`#,##0`)

### [Total Order Items]
```dax
Total Order Items = 
COUNTROWS(fact_order_items)
```
- **Description:** Count of individual line-item rows processed.
- **Format:** Whole Number (`#,##0`)

### [Average Order Value (AOV)]
```dax
Average Order Value = 
DIVIDE(
    [Total Net Sales],
    [Total Orders],
    BLANK()
)
```
- **Description:** Mean net revenue generated per unique customer order.
- **Format:** Currency (`$#,##0.00`)

### [Items Per Order]
```dax
Items Per Order = 
DIVIDE(
    [Total Order Items],
    [Total Orders],
    BLANK()
)
```
- **Description:** Basket depth / average number of lines contained in an order.
- **Format:** Decimal Number (`0.00`)

---

## 3. Shipping & Delivery Performance Measures

### [Total Eligible Shipments]
```dax
Total Eligible Shipments = 
CALCULATE(
    COUNTROWS(fact_order_items),
    fact_order_items[is_eligible_shipment] = 1
)
```
- **Description:** Total delivered orders excluding transit cancellations (`delivery_status <> "Shipping canceled"`).
- **Format:** Whole Number (`#,##0`)

### [Late Delivery Items Count]
```dax
Late Delivery Items Count = 
CALCULATE(
    COUNTROWS(fact_order_items),
    fact_order_items[is_late_delivery] = 1,
    fact_order_items[is_eligible_shipment] = 1
)
```
- **Description:** Number of completed deliveries where transit days exceeded scheduled SLA.
- **Format:** Whole Number (`#,##0`)

### [Late Delivery Rate %]
```dax
Late Delivery Rate % = 
DIVIDE(
    [Late Delivery Items Count],
    [Total Eligible Shipments],
    BLANK()
)
```
- **Description:** Percentage of fulfilled shipments that arrived after the promised delivery date.
- **Format:** Percentage (`0.00%`)

### [On-Time Delivery Rate %]
```dax
On-Time Delivery Rate % = 
1 - [Late Delivery Rate %]
```
- **Description:** Proportion of eligible deliveries arriving on or ahead of scheduled date.
- **Format:** Percentage (`0.00%`)

### [Late Orders Count]
```dax
Late Orders Count = 
CALCULATE(
    DISTINCTCOUNT(fact_order_items[order_id]),
    fact_order_items[is_late_delivery] = 1,
    fact_order_items[is_eligible_shipment] = 1
)
```
- **Description:** Distinct count of orders that had at least one delayed item shipment.
- **Format:** Whole Number (`#,##0`)

### [Late Order Rate %]
```dax
Late Order Rate % = 
DIVIDE(
    [Late Orders Count],
    [Total Orders],
    BLANK()
)
```
- **Description:** Proportion of unique orders experiencing delivery delays.
- **Format:** Percentage (`0.00%`)

### [Average Actual Shipping Days]
```dax
Average Actual Shipping Days = 
AVERAGE(fact_order_items[shipping_days_real])
```
- **Description:** Average recorded shipping duration from dispatch to delivery.
- **Format:** Decimal Number (`0.00`)

### [Average Scheduled Shipping Days]
```dax
Average Scheduled Shipping Days = 
AVERAGE(fact_order_items[shipping_days_scheduled])
```
- **Description:** Average carrier SLA promise duration.
- **Format:** Decimal Number (`0.00`)

### [Average Delay Days (Late Only)]
```dax
Average Delay Days (Late Only) = 
CALCULATE(
    AVERAGE(fact_order_items[delay_days]),
    fact_order_items[is_late_delivery] = 1,
    fact_order_items[is_eligible_shipment] = 1
)
```
- **Description:** Mean number of days overdue for delayed shipments.
- **Format:** Decimal Number (`0.00`)

---

## 4. Time Intelligence & Trend Growth Measures

### [Sales Previous Month]
```dax
Sales Previous Month = 
CALCULATE(
    [Total Net Sales],
    PREVIOUSMONTH(dim_date[full_date])
)
```
- **Description:** Net sales in the immediately preceding calendar month.
- **Format:** Currency (`$#,##0.00`)

### [MoM Net Sales Growth %]
```dax
MoM Net Sales Growth % = 
VAR PrevSales = [Sales Previous Month]
RETURN
DIVIDE(
    [Total Net Sales] - PrevSales,
    PrevSales,
    BLANK()
)
```
- **Description:** Month-over-month sales growth rate.
- **Format:** Percentage (`0.00%`)

### [Profit Previous Month]
```dax
Profit Previous Month = 
CALCULATE(
    [Total Profit],
    PREVIOUSMONTH(dim_date[full_date])
)
```
- **Description:** Realized profit in the preceding month.
- **Format:** Currency (`$#,##0.00`)

### [MoM Profit Growth %]
```dax
MoM Profit Growth % = 
VAR PrevProfit = [Profit Previous Month]
RETURN
DIVIDE(
    [Total Profit] - PrevProfit,
    PrevProfit,
    BLANK()
)
```
- **Description:** Month-over-month profit growth rate.
- **Format:** Percentage (`0.00%`)
