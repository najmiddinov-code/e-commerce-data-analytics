{{ config(
    materialized='table',
    unique_key='customer_id'
)}}

with source as(
    select * from {{ source('raw_ecommerce', 'customers')}}
),
cleaned_customers_data as (
    SELECT
        customer_id,
        INITCAP(TRIM(name)) as customer_name,
        CASE WHEN email NOT LIKE '%@%' THEN 'invalid_email'
             ELSE TRIM(email)
        END AS customer_email,
        TRIM(REGEXP_REPLACE(customer_location, '[0-9!]', '', 'g')) as customer_location,
        created_at
    FROM source
)

SELECT 
    customer_id,
    customer_name,
    customer_email,
    customer_location,
    created_at
FROM cleaned_customers_data
