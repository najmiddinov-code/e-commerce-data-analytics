{{ config(
    materialized='table',
    unique_id='id'
)}}

WITH source AS(
    SELECT *
    FROM {{ source('raw_ecommerce', 'orders') }}
),
cleaned_orders_data AS(
    SELECT
        order_id,
        customer_id,
        product_id,
        CASE WHEN quantity <= 0 THEN 1
             ELSE quantity
        END AS quantity,
        total_price,
        order_date
    FROM source
)

SELECT 
    order_id,
    customer_id,
    product_id,
    quantity,
    total_price,
    order_date
FROM cleaned_orders_data