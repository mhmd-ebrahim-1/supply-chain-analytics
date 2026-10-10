-- =====================================================================
-- 04_regional_analysis.sql
-- Geographic Fulfillment Breakdown, Regional Late Rates, and Revenue
-- =====================================================================

-- 1. Global Market Overview: Sales, Margins, and On-Time Rates
SELECT
    g.market,
    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(f.order_item_id) AS total_items,
    ROUND(SUM(f.net_sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(SUM(f.profit) / SUM(f.net_sales) * 100, 2) AS profit_margin_pct,
    SUM(CASE WHEN f.delivery_status = 'Late delivery' THEN 1 ELSE 0 END) AS late_deliveries,
    ROUND(SUM(CASE WHEN f.delivery_status = 'Late delivery' THEN 1.0 ELSE 0.0 END) / 
          NULLIF(SUM(CASE WHEN f.is_eligible_shipment = 1 THEN 1 ELSE 0 END), 0) * 100, 2) AS late_delivery_rate_pct,
    ROUND(AVG(f.shipping_days_real), 2) AS avg_actual_days,
    ROUND(AVG(f.shipping_days_scheduled), 2) AS avg_scheduled_days
FROM fact_order_items f
JOIN dim_geography g ON f.geography_id = g.geography_id
GROUP BY g.market
ORDER BY total_sales DESC;

-- 2. Destination Region Ranking by Late Delivery Severity
SELECT
    g.order_region,
    g.market,
    COUNT(f.order_item_id) AS total_items,
    SUM(CASE WHEN f.delivery_status = 'Late delivery' THEN 1 ELSE 0 END) AS late_items_count,
    ROUND(SUM(CASE WHEN f.delivery_status = 'Late delivery' THEN 1.0 ELSE 0.0 END) / 
          NULLIF(SUM(CASE WHEN f.is_eligible_shipment = 1 THEN 1 ELSE 0 END), 0) * 100, 2) AS regional_late_rate_pct,
    ROUND(SUM(f.net_sales), 2) AS regional_net_sales,
    ROUND(SUM(f.profit), 2) AS regional_profit,
    ROUND(AVG(f.shipping_days_real - f.shipping_days_scheduled), 2) AS avg_delay_gap_days
FROM fact_order_items f
JOIN dim_geography g ON f.geography_id = g.geography_id
GROUP BY g.order_region, g.market
ORDER BY late_items_count DESC;

-- 3. Top 10 Destination Countries with Largest Fulfillment Volume
SELECT
    g.order_country,
    g.order_region,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.net_sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(SUM(CASE WHEN f.delivery_status = 'Late delivery' THEN 1.0 ELSE 0.0 END) / 
          NULLIF(SUM(CASE WHEN f.is_eligible_shipment = 1 THEN 1 ELSE 0 END), 0) * 100, 2) AS country_late_rate_pct
FROM fact_order_items f
JOIN dim_geography g ON f.geography_id = g.geography_id
GROUP BY g.order_country, g.order_region
ORDER BY total_sales DESC
LIMIT 10;
