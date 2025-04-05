import pandas as pd
import requests

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

def add_salary_after_tax(df):
    """Add a new column for salary after tax."""
    df['Salary_After_Tax'] = df['Salary'] * 0.9
    return df

def save_data(df, filename):
    """Save DataFrame to CSV."""
    df.to_csv(filename, index=False)

def main():
    # Step 1: Read Employee Data
    df = read_employee_data('employees.csv')
    
    # Step 2: Clean Employee Data
    df_cleaned = clean_data(df)
    save_data(df_cleaned, 'cleaned_employees.csv')
    
    # Step 3: Fetch Customer Data
    api_url = "https://jsonplaceholder.typicode.com/users"
    customer_data = fetch_customer_data(api_url)
    
    # Step 4: Identify Customer-Linked Employees
    df_cleaned = identify_customer_linked_employees(df_cleaned, customer_data)
    
    # Step 5: Add Salary After Tax
    df_cleaned = add_salary_after_tax(df_cleaned)
    
    # Step 6: Save Updated Data
    save_data(df_cleaned, 'updated_employees.csv')
    
    # Step 7: Save Customer-Linked Employees
    customer_linked_employees = df_cleaned[df_cleaned['Customer_Linked']]
    save_data(customer_linked_employees, 'customer_linked_employees.csv')
    
    # Step 8: Convert to JSON
    df_cleaned.to_json('employees_data.json', orient='records', indent=4)
    print("ETL process completed successfully!")

if __name__ == '__main__':
    main()