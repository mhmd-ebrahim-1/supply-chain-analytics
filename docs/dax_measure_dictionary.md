# DAX Measure Dictionary: Supply Chain Analytics

Production DAX measures implemented in the Star Schema semantic model (`powerbi/Supply_Chain_Analytics.pbip`).

---

## 1. Financial KPIs

### `[Total Sales]`
```dax
Total Sales = SUM(fact_order_items[sales])
```
- **Description:** Sum of net sales revenue collected from customers across all fulfilled line items.
- **Format:** Currency (`$#,##0.00`)

### `[Total Profit]`
```dax
Total Profit = SUM(fact_order_items[benefit_per_order])
```
- **Description:** Cumulative operating profit contribution across all orders.
- **Format:** Currency (`$#,##0.00`)

### `[Profit Margin %]`
```dax
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)
```
- **Description:** Operating profit margin ratio. Safely handles zero sales.
- **Format:** Percentage (`0.0%`)

### `[AOV]`
```dax
AOV = DIVIDE([Total Sales], [Total Orders], 0)
```
- **Description:** Average Order Value (revenue per distinct checkout transaction).
- **Format:** Currency (`$#,##0.00`)

### `[Total Discount]`
```dax
Total Discount = SUM(fact_order_items[order_item_discount])
```
- **Description:** Total dollar amount granted in promotional discounts.
- **Format:** Currency (`$#,##0.00`)

### `[Avg Discount Rate %]`
```dax
Avg Discount Rate % = AVERAGE(fact_order_items[order_item_discount_rate])
```
- **Description:** Mean promotional discount percentage across line items.
- **Format:** Percentage (`0.0%`)

---

## 2. Operational & Volume KPIs

### `[Total Orders]`
```dax
Total Orders = DISTINCTCOUNT(fact_order_items[order_id])
```
- **Description:** Unique order transactions placed by customers.
- **Format:** Integer (`#,##0`)

### `[Total Quantity]`
```dax
Total Quantity = SUM(fact_order_items[order_item_quantity])
```
- **Description:** Total item units sold across all orders.
- **Format:** Integer (`#,##0`)

---

## 3. Delivery & Fulfillment KPIs

### `[Avg Real Shipping Days]`
```dax
Avg Real Shipping Days = AVERAGE(fact_order_items[days_for_shipping_real])
```
- **Description:** Actual average transit days from dispatch to delivery.
- **Format:** Decimal (`0.00`)

### `[Avg Scheduled Shipping Days]`
```dax
Avg Scheduled Shipping Days = AVERAGE(fact_order_items[days_for_shipment_scheduled])
```
- **Description:** Promised delivery schedule according to shipping SLA.
- **Format:** Decimal (`0.00`)

### `[Shipping Delay Variance]`
```dax
Shipping Delay Variance = [Avg Real Shipping Days] - [Avg Scheduled Shipping Days]
```
- **Description:** Variance between actual transit time and promised delivery schedule (+ indicates delay).
- **Format:** Decimal (`+0.00;-0.00;0.00`)

### `[Late Delivery Orders]`
```dax
Late Delivery Orders = CALCULATE([Total Orders], fact_order_items[late_delivery_risk] = 1)
```
- **Description:** Number of unique orders experiencing delivery delay.
- **Format:** Integer (`#,##0`)

### `[Late Delivery Rate %]`
```dax
Late Delivery Rate % = DIVIDE([Late Delivery Orders], [Total Orders], 0)
```
- **Description:** Proportion of total orders that arrived past the scheduled SLA.
- **Format:** Percentage (`0.0%`)

### `[On-Time Delivery Rate %]`
```dax
On-Time Delivery Rate % = 
DIVIDE(
    CALCULATE([Total Orders], dim_shipping[delivery_status] IN { "Shipping on time", "Advance shipping" }),
    [Total Orders],
    0
)
```
- **Description:** Proportion of orders delivered strictly on or ahead of schedule.
- **Format:** Percentage (`0.0%`)

---

## 4. Customer & Geography Intelligence

### `[Active Customers]`
```dax
Active Customers = DISTINCTCOUNT(fact_order_items[customer_id])
```
- **Description:** Unique customers with placed orders.
- **Format:** Integer (`#,##0`)

### `[Sales per Customer]`
```dax
Sales per Customer = DIVIDE([Total Sales], [Active Customers], 0)
```
- **Description:** Average revenue contribution per customer account.
- **Format:** Currency (`$#,##0.00`)

### `[Countries Reached]`
```dax
Countries Reached = DISTINCTCOUNT(dim_geography[order_country])
```
- **Description:** Number of unique destination countries fulfilled.
- **Format:** Integer (`#,##0`)

### `[Suspected Fraud Orders]`
```dax
Suspected Fraud Orders = CALCULATE([Total Orders], dim_order[order_status] = "SUSPECTED_FRAUD")
```
- **Description:** Orders flagged under suspected fraud security review.
- **Format:** Integer (`#,##0`)

---

## 5. Product Performance

### `[Active Products]`
```dax
Active Products = DISTINCTCOUNT(fact_order_items[product_id])
```
- **Description:** Number of unique catalog products with transaction history.
- **Format:** Integer (`#,##0`)
