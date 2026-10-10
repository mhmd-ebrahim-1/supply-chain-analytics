# Data Quality & Anomaly Report: DataCo Supply Chain Dataset

## 1. Executive Summary

This report documents the rigorous data profiling, quality checks, and structural anomalies identified in the **DataCo Smart Supply Chain for Big Data Analysis** dataset (180,519 rows, 53 columns).

Every issue is categorized as either a **Confirmed Issue** (empirically validated in raw records) or a **Potential Risk / Modeling Consideration**.

---

## 2. Confirmed Data Quality Issues

| # | Anomaly Type | Columns Affected | Magnitude | Impact on Analysis | Treatment / Resolution Rule |
|---|---|---|---|---|---|
| **CQ-01** | **Character Encoding Incompatibility** | All textual columns | 180,519 rows | Reading with `UTF-8` fails with decode error (`0xe1` in position 6) due to Spanish and Puerto Rican accents (e.g., Caguas, Mayagüez). | Force explicit `latin1` / `ISO-8859-1` encoding during ingestion, followed by normalization to clean UTF-8. |
| **CQ-02** | **Complete Structural Column Nullity** | `Product Description` | 180,519 rows (100.0%) | Contains zero analytical information. | Drop column from analytical fact and dimension models. |
| **CQ-03** | **High Sparsity in Destination Postal Codes** | `Order Zipcode` | 155,679 rows (86.24%) | Destination postal codes are unavailable for international and many regional destinations. | Drop `Order Zipcode` from primary dimensional hierarchy; rely on `Order Region`, `Order Country`, `Order State`, and `Order City` which have 100% completeness. |
| **CQ-04** | **Minor Customer Nulls** | `Customer Zipcode` (3 rows), `Customer Lname` (8 rows) | 11 rows total (< 0.01%) | Extremely minor missingness in customer profile attributes. | Impute `Customer Zipcode` as `'Unknown'` / 0; impute `Customer Lname` as `'Unknown'`. Do not delete records. |
| **CQ-05** | **Exact Column Redundancy & Synonyms** | `Benefit per order` vs `Order Profit Per Order`<br>`Category Id` vs `Product Category Id`<br>`Customer Id` vs `Order Customer Id`<br>`Product Card Id` vs `Order Item Cardprod Id` | 180,519 rows (100% match) | Creates schema bloat and potential confusion for BI developers. | Deduplicate during data modeling. Keep standardized business names (`profit`, `product_id`, `customer_id`, `category_id`). |
| **CQ-06** | **Delivery Status vs Late Risk Discordance** | `Delivery Status`, `Late_delivery_risk` | 7,754 rows (`Shipping canceled`) | `Late_delivery_risk` is coded as `0` for all canceled shipments, even though 4,423 of them exceeded scheduled days before cancellation. | Define **Shipment Eligibility Rule**: For delivery performance KPIs (On-Time Delivery Rate, Late Delivery Rate), filter strictly to eligible completed/shipped deliveries (`Delivery Status != 'Shipping canceled'`). |
| **CQ-07** | **Incomplete Final Year Time-Series Truncation** | `order date (DateOrders)` | 2,123 rows (Jan 2018) | 2018 contains only 1 month (January 1 - January 31, 2018), while 2015-2017 are complete calendar years. | Do not compare annual totals of 2018 to full preceding years without run-rate adjustments or monthly segmentation. |
| **CQ-08** | **Zero-Variance / Uninformative Stock Column** | `Product Status` | 180,519 rows (100% value `0`) | Provides zero variance. Does not represent actual warehouse balances. | Retain as catalog flag or drop; explicitly document that inventory stockouts cannot be measured from this field. |

---

## 3. Financial & Calculation Consistency Checks

Empirical validation of calculated columns vs raw financial metrics:

```python
# Formulas tested:
Gross_Sales = Order Item Product Price * Order Item Quantity
Net_Sales = Gross_Sales - Order Item Discount
Profit_Ratio = Benefit per order / Order Item Total
```

### Empirical Results:
1. **Gross Sales vs `Sales`:**
   - Max absolute difference: `$0.00002` (floating point rounding). `Sales` equals gross product value before discount.
2. **Net Sales vs `Order Item Total`:**
   - Max absolute difference: `$0.01` (standard cent rounding). `Order Item Total` is true net cash collected.
3. **Profit vs `Order Profit Per Order`:**
   - Exact identity (`0.00` difference).
4. **Negative Profit Items:**
   - **43,710 rows (24.21%)** have negative profit (`Order Profit Per Order < 0`).
   - Root cause: Substantial discounts applied (up to 25% discount rate) without price adjustments, eroding margins below cost of goods sold.

---

## 4. Potential Risks & Modeling Considerations

### A. Target Leakage Risk in Delivery Predictive Modeling
- Predictive models for `Late_delivery_risk` or `Delivery Status` **must not** use features determined after order placement:
  - `Days for shipping (real)` (direct outcome leakage)
  - `shipping date (DateOrders)` (future timestamp)
  - `Delivery Status` (target proxy)
- Permissible predictors are strictly operational features known at order creation:
  - `Shipping Mode`, `Days for shipment (scheduled)`, `Order Region`, `Market`, `Order Item Quantity`, `Order Item Total`, `Category Id`, `Department Id`, order date temporal features (hour, day of week, month).

### B. Order vs Item Aggregation Pitfall
- Multiple items belong to the same `Order Id` (65,752 orders vs 180,519 items).
- Summing `Benefit per order` across all items is valid for total profit because `Benefit per order` is actually recorded per item (item-level profit contribution despite the misleading column label).
- However, counting distinct orders requires `COUNT(DISTINCT Order Id)` to prevent double-counting order volume by a factor of 2.75x.

---

## 5. Summary Quality Assessment

The DataCo dataset is of **high analytical utility for supply chain logistics, fulfillment timeliness, customer geographic segmentation, and product profitability**. It does **not** support direct warehouse inventory optimization without supplementary inventory datasets.
