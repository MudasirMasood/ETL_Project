CREATE TABLE silver.department_employee_count (
    department NVARCHAR(100),
    employee_count INT
);
GO
INSERT INTO silver.department_employee_count (department, employee_count)
SELECT 
    department,
    COUNT(*) AS employee_count
FROM 
    raw.stg_employees
WHERE 
    salary > 0  -- Clean data by excluding zero salaries
GROUP BY 
    department;
GO