{{ config(
    materialized='table'
) }}

WITH orders AS (
    SELECT *
    FROM {{ ref('stg_orders') }}
),

products AS (
    SELECT *
    FROM {{ ref('stg_products') }}
),

customers AS (
    SELECT *
    FROM {{ ref('stg_customers') }}
)

SELECT
    o.order_id,
    o.customer_id,
    c.customer_name,
    c.customer_email,
    c.customer_location,

    o.product_id,
    p.product_name,
    p.product_category,
    p.price,

    o.quantity,
    p.price * o.quantity AS total_price,
    o.order_date

FROM orders o
LEFT JOIN products p ON o.product_id = p.product_id
LEFT JOIN customers c ON o.customer_id = c.customer_id

WHERE p.price IS NOT NULL