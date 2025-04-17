-- Create the staging table
CREATE TABLE raw.stg_employees (
    id INT,
    name NVARCHAR(100),
    age INT,
    department NVARCHAR(100),
    salary DECIMAL(10, 2)
);

-- Load data from CSV
BULK INSERT raw.stg_employees
FROM 'C:\Users\TECH CLOUD\Desktop\ETL_PROJECT\raw\stg_employees.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);