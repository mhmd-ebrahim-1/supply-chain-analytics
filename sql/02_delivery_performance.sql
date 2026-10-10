-- =====================================================================
-- 02_delivery_performance.sql
-- Carrier Timeliness, Shipping Mode SLA Benchmark, and Delay Diagnostics
-- =====================================================================

-- 1. Carrier Shipping Mode Performance Summary (Eligible Shipments)
-- Calculates On-Time Rate, Late Rate, and SLA Duration Gaps
SELECT
    shipping_mode,
    COUNT(order_item_id) AS total_shipments,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(CASE WHEN delivery_status = 'Late delivery' THEN 1 ELSE 0 END) AS late_shipment_count,
    ROUND(SUM(CASE WHEN delivery_status = 'Late delivery' THEN 1.0 ELSE 0.0 END) / COUNT(order_item_id) * 100, 2) AS late_item_rate_pct,
    ROUND(COUNT(DISTINCT CASE WHEN delivery_status = 'Late delivery' THEN order_id END)::DOUBLE / COUNT(DISTINCT order_id) * 100, 2) AS late_order_rate_pct,
    ROUND(AVG(shipping_days_real), 2) AS avg_actual_shipping_days,
    ROUND(AVG(shipping_days_scheduled), 2) AS avg_scheduled_shipping_days,
    ROUND(AVG(shipping_days_real - shipping_days_scheduled), 2) AS avg_transit_variance_days
FROM fact_order_items
WHERE is_eligible_shipment = 1
GROUP BY shipping_mode
ORDER BY total_shipments DESC;

-- 2. Delivery Status Matrix Breakdown (Including Cancellations)
SELECT
    delivery_status,
    COUNT(order_item_id) AS item_count,
    ROUND(COUNT(order_item_id)::DOUBLE / SUM(COUNT(order_item_id)) OVER() * 100, 2) AS pct_of_total_items,
    ROUND(AVG(shipping_days_real), 2) AS avg_actual_days,
    ROUND(AVG(shipping_days_scheduled), 2) AS avg_scheduled_days,
    ROUND(AVG(CASE WHEN delay_days > 0 THEN delay_days ELSE NULL END), 2) AS avg_overdue_days_when_late
FROM fact_order_items
GROUP BY delivery_status
ORDER BY item_count DESC;

-- 3. Transit Delay Distribution for Overdue Orders
WITH delay_brackets AS (
    SELECT
        order_item_id,
        delay_days,
        CASE
            WHEN delay_days <= 0 THEN '0. On-Time or Early'
            WHEN delay_days = 1 THEN '1. 1 Day Overdue'
            WHEN delay_days = 2 THEN '2. 2 Days Overdue'
            WHEN delay_days = 3 THEN '3. 3 Days Overdue'
            ELSE '4. 4+ Days Overdue'
        END AS delay_category
    FROM fact_order_items
    WHERE is_eligible_shipment = 1
)
SELECT
    delay_category,
    COUNT(*) AS shipment_count,
    ROUND(COUNT(*)::DOUBLE / SUM(COUNT(*)) OVER() * 100, 2) AS percentage_of_eligible_deliveries
FROM delay_brackets
GROUP BY delay_category
ORDER BY delay_category;
