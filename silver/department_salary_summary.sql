CREATE TABLE silver.department_salary_summary (
    department NVARCHAR(100),
    average_salary DECIMAL(10, 2)
);
GO
INSERT INTO silver.department_salary_summary (department, average_salary)
SELECT 
    department,
    AVG(salary) AS average_salary
FROM 
    raw.stg_employees
WHERE 
    salary > 0  -- Clean data by excluding zero salaries
GROUP BY 
    department;
GO