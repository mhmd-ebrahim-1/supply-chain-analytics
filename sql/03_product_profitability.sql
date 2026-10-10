-- =====================================================================
-- 03_product_profitability.sql
-- Product Catalog Margins, Category Profitability, and Discount Erosion
-- =====================================================================

-- 1. Category-Level Performance & Profit Margins
SELECT
    p.category_name,
    p.department_name,
    COUNT(f.order_item_id) AS total_units_sold,
    ROUND(SUM(f.net_sales), 2) AS total_net_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(SUM(f.profit) / SUM(f.net_sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(f.order_item_discount_rate) * 100, 2) AS avg_discount_rate_pct,
    SUM(CASE WHEN f.profit < 0 THEN 1 ELSE 0 END) AS loss_making_transactions_count,
    ROUND(SUM(CASE WHEN f.profit < 0 THEN 1.0 ELSE 0.0 END) / COUNT(f.order_item_id) * 100, 2) AS pct_transactions_unprofitable
FROM fact_order_items f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category_name, p.department_name
ORDER BY total_net_sales DESC;

-- 2. Top 15 Products by Revenue vs Profit Margin
WITH product_performance AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category_name,
        p.abc_revenue_class,
        COUNT(f.order_item_id) AS volume_sold,
        ROUND(SUM(f.net_sales), 2) AS total_sales,
        ROUND(SUM(f.profit), 2) AS total_profit,
        ROUND(SUM(f.profit) / SUM(f.net_sales) * 100, 2) AS margin_pct,
        DENSE_RANK() OVER (ORDER BY SUM(f.net_sales) DESC) AS revenue_rank,
        DENSE_RANK() OVER (ORDER BY SUM(f.profit) DESC) AS profit_rank
    FROM fact_order_items f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category_name, p.abc_revenue_class
)
SELECT
    revenue_rank,
    profit_rank,
    product_name,
    category_name,
    abc_revenue_class,
    volume_sold,
    total_sales,
    total_profit,
    margin_pct,
    (revenue_rank - profit_rank) AS rank_delta -- Positive indicates profit underperforming revenue
FROM product_performance
ORDER BY revenue_rank ASC
LIMIT 15;

-- 3. High-Sales, Low-Margin Products Diagnostic
-- Identifies products in Top 30% by sales with below-average profitability
WITH catalog_benchmarks AS (
    SELECT
        AVG(profit / net_sales) AS portfolio_avg_margin
    FROM fact_order_items
    WHERE net_sales > 0
),
ranked_products AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category_name,
        ROUND(SUM(f.net_sales), 2) AS total_sales,
        ROUND(SUM(f.profit), 2) AS total_profit,
        ROUND(SUM(f.profit) / SUM(f.net_sales) * 100, 2) AS margin_pct,
        NTILE(5) OVER (ORDER BY SUM(f.net_sales) DESC) AS sales_quintile
    FROM fact_order_items f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category_name
)
SELECT
    r.product_name,
    r.category_name,
    r.total_sales,
    r.total_profit,
    r.margin_pct
FROM ranked_products r
CROSS JOIN catalog_benchmarks b
WHERE r.sales_quintile = 1 -- Top 20% in sales volume
  AND (r.margin_pct / 100.0) < b.portfolio_avg_margin
ORDER BY r.total_sales DESC;

-- 4. Impact of Discounting Tiers on Line-Item Profitability
SELECT
    f.discount_tier,
    COUNT(*) AS total_items,
    ROUND(SUM(f.net_sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND(AVG(f.profit), 2) AS avg_profit_per_item,
    ROUND(SUM(f.profit) / SUM(f.net_sales) * 100, 2) AS margin_pct,
    ROUND(SUM(CASE WHEN f.profit < 0 THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) AS pct_negative_profit_orders
FROM fact_order_items f
GROUP BY f.discount_tier
ORDER BY f.discount_tier;
