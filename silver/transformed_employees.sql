CREATE VIEW silver.transformed_employees AS
SELECT 
    id,
    name,
    age,
    department,
    ROUND(AVG(salary), 2) AS average_salary
FROM 
    raw.stg_employees
WHERE 
    salary > 0  -- Clean data by excluding zero salaries
GROUP BY 
    id, name, age, department;
GO