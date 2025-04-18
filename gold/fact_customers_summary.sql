CREATE TABLE fact_customers_summary AS
SELECT 
    customer_id,
    COUNT(order_id) AS total_orders
FROM 
    stg_orders
GROUP BY 
    customer_id;