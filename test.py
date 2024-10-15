import pandas as pd
import mysql.connector
import os

# Configuration
sql_file_path = 'sql_file.sql'  # Path to your SQL file
database_name = 'littlelemon'        # Your database name
host = 'localhost'                     # Your MySQL host
user = 'root'                          # Your MySQL username
password = '12345'             # Your MySQL password
output_excel_file = 'output.xlsx'     # Desired output Excel file name

# Function to read SQL file
def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Connect to MySQL
connection = mysql.connector.connect(
    host=host,
    database=database_name,
    user=user,
    password=password
)

cursor = connection.cursor()

# Read the SQL file
sql_commands = read_sql_file(sql_file_path)

# Execute SQL commands
try:
    # Split the SQL commands into individual statements
    for command in sql_commands.split(';'):
        if command.strip():  # Ignore empty commands
            cursor.execute(command)
    # Commit changes if there were any INSERT statements
    connection.commit()
except Exception as e:
    print(f"Error executing SQL commands: {e}")
finally:
    cursor.close()
    connection.close()

# Reconnect to MySQL to fetch data
connection = mysql.connector.connect(
    host=host,
    database=database_name,
    user=user,
    password=password
)

# Load data from the database into a DataFrame
tables = pd.read_sql("SHOW TABLES;", connection)

# Create an Excel writer
with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
    for table in tables.values:
        table_name = table[0]
        df = pd.read_sql(f"SELECT * FROM {table_name};", connection)
        df.to_excel(writer, sheet_name=table_name, index=False)

# Close the connection
connection.close()

print(f"Data has been exported to {output_excel_file}.")
