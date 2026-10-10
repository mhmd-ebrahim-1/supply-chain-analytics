-- =====================================================================
-- 01_data_quality.sql
-- Data Quality Auditing, Primary Key Integrity, and Grain Reconciliation
-- =====================================================================

-- 1. Primary Key Uniqueness and Grain Verification
-- Verifies that order_item_id is the primary key (1 row per item)
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_item_id) AS unique_order_items,
    COUNT(DISTINCT order_id) AS unique_orders,
    ROUND(COUNT(*)::DOUBLE / COUNT(DISTINCT order_id), 2) AS avg_items_per_order
FROM fact_order_items;

-- 2. Completeness & Critical Field Null Audits
SELECT
    COUNT(*) - COUNT(order_item_id) AS null_order_item_ids,
    COUNT(*) - COUNT(order_id) AS null_order_ids,
    COUNT(*) - COUNT(customer_id) AS null_customer_ids,
    COUNT(*) - COUNT(product_id) AS null_product_ids,
    COUNT(*) - COUNT(net_sales) AS null_net_sales,
    COUNT(*) - COUNT(profit) AS null_profit,
    COUNT(*) - COUNT(shipping_mode) AS null_shipping_modes,
    COUNT(*) - COUNT(delivery_status) AS null_delivery_statuses
FROM fact_order_items;

-- 3. Financial Formula Identity Reconciliation
-- Checks whether Net Sales = Gross Sales - Discount across all line items
WITH financial_check AS (
    SELECT
        order_item_id,
        gross_sales,
        order_item_discount,
        net_sales,
        ROUND((gross_sales - order_item_discount)::NUMERIC, 2) AS calculated_net_sales,
        ABS(net_sales - (gross_sales - order_item_discount)) AS discrepancy
    FROM fact_order_items
)
SELECT
    COUNT(*) AS total_checked,
    MAX(discrepancy) AS max_absolute_discrepancy,
    SUM(CASE WHEN discrepancy > 0.05 THEN 1 ELSE 0 END) AS failed_records
FROM financial_check;

-- 4. Order-Level vs Item-Level Reconciliation
-- Demonstrates why distinct order counts must be used to avoid duplication
SELECT
    COUNT(order_item_id) AS line_item_count,
    COUNT(DISTINCT order_id) AS distinct_order_count,
    ROUND(SUM(net_sales), 2) AS total_realized_sales,
    ROUND(SUM(profit), 2) AS total_realized_profit,
    ROUND(SUM(net_sales) / COUNT(DISTINCT order_id), 2) AS average_order_value_aov,
    ROUND(SUM(profit) / SUM(net_sales) * 100, 2) AS portfolio_profit_margin_pct
FROM fact_order_items;
