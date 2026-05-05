{{ config(
    materialized='table'
) }}

WITH sales AS (
    SELECT *
    FROM {{ ref('mart_sales_detail') }}
)

SELECT
    product_category,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(quantity) AS total_quantity,
    SUM(total_price) AS total_revenue,
    AVG(total_price) AS avg_order_value
FROM sales
GROUP BY product_category