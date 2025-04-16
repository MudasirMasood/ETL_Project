CREATE TABLE gold.department_salary_summary AS
SELECT 
    department,
    AVG(salary) AS average_salary
FROM 
    silver.transformed_employees
GROUP BY 
    department;