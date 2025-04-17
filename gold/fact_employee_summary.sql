CREATE TABLE gold.fact_employee_summary AS
SELECT 
    id,
    name,
    age,
    department,
    ROUND(AVG(salary), 2) AS average_salary
FROM 
    silver.transformed_employees
GROUP BY 
    id, name, age, department;
GO