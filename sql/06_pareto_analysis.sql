-- =====================================================================
-- 06_pareto_analysis.sql
-- 80/20 Pareto Concentration: Late Deliveries, Products, and Profit Contribution
-- =====================================================================

-- 1. Regional Late Shipment Concentration (Pareto Principle)
-- Checks whether a minority of regions account for ~80% of late shipments
WITH regional_lates AS (
    SELECT
        g.order_region,
        g.market,
        COUNT(f.order_item_id) AS total_shipments,
        SUM(CASE WHEN f.delivery_status = 'Late delivery' THEN 1 ELSE 0 END) AS late_shipments
    FROM fact_order_items f
    JOIN dim_geography g ON f.geography_id = g.geography_id
    WHERE f.is_eligible_shipment = 1
    GROUP BY g.order_region, g.market
),
cumulative_calc AS (
    SELECT
        order_region,
        market,
        total_shipments,
        late_shipments,
        ROUND(late_shipments::DOUBLE / total_shipments * 100, 2) AS regional_late_rate_pct,
        SUM(late_shipments) OVER (ORDER BY late_shipments DESC) AS cumulative_late_shipments,
        SUM(late_shipments) OVER () AS total_network_late_shipments
    FROM regional_lates
)
SELECT
    order_region,
    market,
    late_shipments,
    regional_late_rate_pct,
    cumulative_late_shipments,
    ROUND(cumulative_late_shipments::DOUBLE / total_network_late_shipments * 100, 2) AS cumulative_late_share_pct,
    CASE
        WHEN cumulative_late_shipments::DOUBLE / total_network_late_shipments <= 0.80 THEN 'Top 80% Late Drivers'
        ELSE 'Long Tail'
    END AS pareto_classification
FROM cumulative_calc
ORDER BY late_shipments DESC;

-- 2. Product Revenue Pareto Contribution (ABC Stratification)
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category_name,
        ROUND(SUM(f.net_sales), 2) AS total_product_sales,
        ROUND(SUM(f.profit), 2) AS total_product_profit
    FROM fact_order_items f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category_name
),
cumulative_revenue AS (
    SELECT
        product_id,
        product_name,
        category_name,
        total_product_sales,
        total_product_profit,
        SUM(total_product_sales) OVER (ORDER BY total_product_sales DESC) AS running_total_sales,
        SUM(total_product_sales) OVER () AS catalog_total_sales
    FROM product_revenue
)
SELECT
    product_name,
    category_name,
    total_product_sales,
    total_product_profit,
    ROUND(running_total_sales / catalog_total_sales * 100, 2) AS cumulative_sales_pct,
    CASE
        WHEN running_total_sales / catalog_total_sales <= 0.70 THEN 'Class A (Top 70%)'
        WHEN running_total_sales / catalog_total_sales <= 0.90 THEN 'Class B (70-90%)'
        ELSE 'Class C (Bottom 10%)'
    END AS abc_class
FROM cumulative_revenue
ORDER BY total_product_sales DESC;
