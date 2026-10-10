-- =====================================================================
-- 05_time_series_analysis.sql
-- Monthly Seasonality, Growth Trajectories, and Fulfillments Over Time
-- =====================================================================

-- 1. Monthly Performance Time-Series with Month-over-Month (MoM) Growth
WITH monthly_metrics AS (
    SELECT
        d.year,
        d.month,
        d.year_month,
        COUNT(DISTINCT f.order_id) AS monthly_orders,
        COUNT(f.order_item_id) AS monthly_items,
        ROUND(SUM(f.net_sales), 2) AS monthly_sales,
        ROUND(SUM(f.profit), 2) AS monthly_profit,
        ROUND(SUM(CASE WHEN f.delivery_status = 'Late delivery' THEN 1.0 ELSE 0.0 END) / 
              NULLIF(SUM(CASE WHEN f.is_eligible_shipment = 1 THEN 1 ELSE 0 END), 0) * 100, 2) AS monthly_late_rate_pct
    FROM fact_order_items f
    JOIN dim_date d ON f.order_date_key = d.date_key
    GROUP BY d.year, d.month, d.year_month
),
mom_growth AS (
    SELECT
        year_month,
        monthly_orders,
        monthly_items,
        monthly_sales,
        monthly_profit,
        monthly_late_rate_pct,
        LAG(monthly_sales) OVER (ORDER BY year_month) AS prev_month_sales,
        LAG(monthly_profit) OVER (ORDER BY year_month) AS prev_month_profit
    FROM monthly_metrics
)
SELECT
    year_month,
    monthly_orders,
    monthly_items,
    monthly_sales,
    monthly_profit,
    ROUND((monthly_sales - prev_month_sales) / NULLIF(prev_month_sales, 0) * 100, 2) AS mom_sales_growth_pct,
    ROUND((monthly_profit - prev_month_profit) / NULLIF(prev_month_profit, 0) * 100, 2) AS mom_profit_growth_pct,
    monthly_late_rate_pct
FROM mom_growth
ORDER BY year_month ASC;

-- 2. Day-of-Week Seasonality and Delivery Performance
SELECT
    d.day_of_week,
    COUNT(DISTINCT f.order_id) AS orders_placed,
    ROUND(SUM(f.net_sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(SUM(CASE WHEN f.delivery_status = 'Late delivery' THEN 1.0 ELSE 0.0 END) / 
          NULLIF(SUM(CASE WHEN f.is_eligible_shipment = 1 THEN 1 ELSE 0 END), 0) * 100, 2) AS late_rate_pct
FROM fact_order_items f
JOIN dim_date d ON f.order_date_key = d.date_key
GROUP BY d.day_of_week
ORDER BY orders_placed DESC;
