BULK INSERT raw.stg_employees
FROM 'C:\Users\TECH CLOUD\Desktop\ETL_PROJECT\stg_employees.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);