CREATE TABLE fact_orders_summary AS
SELECT 
    customer_name,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM 
    transformed_orders
GROUP BY 
    customer_name;