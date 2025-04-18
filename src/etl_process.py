import pandas as pd
import requests
import sqlite3
import os

def read_employee_data(file_path):
    """Read employee data from a CSV file."""
    return pd.read_csv(file_path)

def clean_data(df):
    """Remove duplicates and fill missing salaries."""
    df_cleaned = df.drop_duplicates()
    df_cleaned['Salary'] = df_cleaned['Salary'].fillna(df_cleaned['Salary'].mean())
    return df_cleaned

def fetch_customer_data(api_url):
    """Fetch customer data from the API."""
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def identify_customer_linked_employees(df, customer_data):
    """Identify employees who work in customer companies."""
    customer_companies = {user['company']['name'] for user in customer_data}
    df['Customer_Linked'] = df['Department'].isin(customer_companies)
    return df

def filter_employees(df):
    """Filter employees older than 30."""
    return df[df['Age'] > 30]

def add_salary_after_tax(df):
    """Add a new column for salary after tax using vectorized operations."""
    df = df.copy()  # Create a copy to avoid SettingWithCopyWarning
    df['Salary_After_Tax'] = df['Salary'] * 0.9  # Direct calculation
    return df

def write_csv(df, filename):
    """Save DataFrame to CSV."""
    df.to_csv(filename, index=False)

def load_data_to_db(data, db_name):
    """Load the transformed data into a SQLite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create employee table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Email TEXT,
            Department TEXT,
            Salary REAL,
            Salary_After_Tax REAL,
            Customer_Linked BOOLEAN
        )
    ''')

    # Insert data into employees table
    # Your existing insertion logic...

    # Drop existing views if they exist
    cursor.execute('DROP VIEW IF EXISTS transformed_orders')
    cursor.execute('DROP TABLE IF EXISTS fact_orders_summary')
    cursor.execute('DROP TABLE IF EXISTS dim_customers')

    # Create new views and tables
    cursor.execute('''
    CREATE VIEW transformed_orders AS
    SELECT 
        o.order_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        o.order_date,
        SUM(oi.quantity) AS total_items,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_amount,
        o.status
    FROM 
        stg_orders o
    JOIN 
        stg_order_items oi ON o.order_id = oi.order_id
    JOIN 
        stg_customers c ON o.customer_id = c.customer_id
    WHERE 
        o.status = 'delivered'
    GROUP BY 
        o.order_id, c.first_name, c.last_name, o.order_date, o.status;
    ''')

    # Create final tables
    cursor.execute('''
    CREATE TABLE fact_orders_summary AS
    SELECT 
        customer_name,
        COUNT(order_id) AS total_orders,
        SUM(total_amount) AS total_revenue
    FROM 
        transformed_orders
    GROUP BY 
        customer_name;
    ''')

    cursor.execute('''
    CREATE TABLE dim_customers AS
    SELECT 
        customer_id,
        first_name || ' ' || last_name AS customer_name,
        signup_date
    FROM 
        stg_customers;
    ''')

    conn.commit()
    conn.close()

def main():
    try:
        # Ensure output directory exists
        os.makedirs('output', exist_ok=True)

        # Step 1: Read Employee Data
        df = read_employee_data('input/employees.csv')
        
        # Step 2: Clean Employee Data
        df_cleaned = clean_data(df)
        write_csv(df_cleaned, 'output/cleaned_employees.csv')
        
        # Step 3: Fetch Customer Data
        api_url = "https://jsonplaceholder.typicode.com/users"  # Example API URL
        customer_data = fetch_customer_data(api_url)
        
        # Step 4: Identify Customer-Linked Employees
        df_cleaned = identify_customer_linked_employees(df_cleaned, customer_data)
        
        # Step 5: Filter Employees Older Than 30
        df_filtered = filter_employees(df_cleaned)
        
        # Step 6: Add Salary After Tax
        df_filtered = add_salary_after_tax(df_filtered)
        
        # Step 7: Save Updated Data
        write_csv(df_filtered, 'output/updated_employees.csv')
        
        # Step 8: Save Customer-Linked Employees
        customer_linked_employees = df_filtered[df_filtered['Customer_Linked']]
        write_csv(customer_linked_employees, 'output/customer_linked_employees.csv')
        
        # Step 9: Convert to JSON
        df_filtered.to_json('output/employees_data.json', orient='records', indent=4)
        
        # Step 10: Load Data to SQLite
        load_data_to_db(df_filtered.to_dict(orient='records'), 'employees.db')

        print("ETL process completed successfully!")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    main()