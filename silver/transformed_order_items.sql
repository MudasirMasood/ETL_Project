CREATE VIEW transformed_order_items AS
SELECT 
    order_id,
    SUM(quantity) AS total_quantity,
    SUM(quantity * unit_price) AS total_value
FROM 
    stg_order_items
GROUP BY 
    order_id;