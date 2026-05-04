{{ config(
    materialized='table',
    unique_key='id'
)}}

WITH source AS(
    SELECT
        *
    FROM {{ source('raw_ecommerce', 'products') }}
),
cleaned_products_data AS(
    SELECT
        product_id,
        INITCAP(TRIM(name)) AS product_name,
        CASE WHEN product_category NOT IN ('Electronics', 'Clothing', 'Home', 'Toys', 'Books') THEN 'Other'
             ELSE product_category
        END as product_category,
        CASE WHEN price > 10000 THEN NULL
             ELSE ABS(price)
        END AS price,
        created_at
    FROM source
             
)

SELECT * FROM cleaned_products_data