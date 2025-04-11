# ETL Project

## Overview
This project is an ETL (Extract, Transform, Load) pipeline that processes employee data. It extracts employee information from a CSV file, transforms the data (cleaning and filtering), and loads it into a SQLite database.

## Features
- **Data Extraction**: Reads employee data from a CSV file.
- **Data Transformation**: Cleans the data by removing duplicates, filling missing salary values, and filtering employees based on age.
- **Data Loading**: Loads the cleaned data into a SQLite database.
- **Customer Linkage**: Identifies employees linked to customer companies from an external API.

## Requirements
To run this project, you need to install the necessary dependencies. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt


File Structure
The project has the following structure:

ETL_PROJECT/
├── input
│   └── employees.csv          # Input file containing employee data
├── output
│   ├── cleaned_employees.csv  # Cleaned employee data
│   ├── updated_employees.csv   # Updated employee data after transformations
│   ├── customer_linked_employees.csv # Employees linked to customers
│   └── employees_data.json     # JSON representation of employee data
├── src
│   └── etl_process.py         # Main script for the ETL process
├── requirements.txt           # List of dependencies
└── README.md                  # Documentation for the project

How to Run the Project
Prepare Your Environment:
Ensure you have Python installed on your machine.
Create a virtual environment (optional but recommended):
python -m venv venv

Activate the virtual environment:
On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

Install Dependencies:
Run the following command:

pip install -r requirements.txt

Run the ETL Process:
Execute the main script:

python src/etl_process.py

License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.