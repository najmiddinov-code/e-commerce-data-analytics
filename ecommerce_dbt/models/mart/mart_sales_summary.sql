{{ config(
    materialized='table'
)}}

SELECT 
    c.customer_name,
    c.customer_email,
    c.customer_location,
    p.product_name,
    p.product_category,
    p.price,
    o.order_id,
    o.quantity,
    o.total_price
FROM {{ ref('stg_orders') }} AS o
LEFT JOIN {{ ref('stg_products') }} AS p
ON o.product_id = p.product_id
LEFT JOIN {{ ref('stg_customers') }} AS c
ON c.customer_id = o.customer_id