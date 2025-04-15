SELECT 
    department,
    AVG(salary) AS average_salary
INTO gold.department_salary_summary
FROM silver.transformed_employees
GROUP BY department;