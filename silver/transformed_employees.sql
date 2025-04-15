CREATE VIEW silver.transformed_employees AS
SELECT 
    id,
    name,
    age,
    department,
    ROUND(salary, 2) AS salary
FROM 
    raw.stg_employees;