import pandas as pd
import mysql.connector

# Load the Excel file
file_path = 'littlelemon.xlsx'  # Change this to your file path
data = pd.read_excel(file_path)

# Clean the data: Remove leading/trailing spaces and handle NaN values
data.columns = data.columns.str.strip()  # Strip whitespace from column names
data.fillna('', inplace=True)  # Replace NaN with empty strings

# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',  # Change if necessary
    database='littlelemon',  # Your database name
    user='root',  # Your username
    password='12345'  # Your password
)

cursor = connection.cursor()

# Insert customers into the database
for _, row in data.iterrows():
    cursor.execute("""
        INSERT INTO customers (customer_id, customer_name, city, country, postal_code, country_code)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            customer_name = VALUES(customer_name), 
            city = VALUES(city), 
            country = VALUES(country), 
            postal_code = VALUES(postal_code), 
            country_code = VALUES(country_code);
    """, (row['Customer ID'], row['Customer Name'], row['City'], row['Country'], row['Postal Code'], row['Country Code']))

# Insert courses into the database
for _, row in data.iterrows():
    cursor.execute("""
        INSERT INTO courses (course_name, cuisine_name, starter_name, desert_name, drink, sides)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            cuisine_name = VALUES(cuisine_name), 
            starter_name = VALUES(starter_name), 
            desert_name = VALUES(desert_name), 
            drink = VALUES(drink), 
            sides = VALUES(sides);
    """, (row['Course Name'], row['Cuisine Name'], row['Starter Name'], row['Desert Name'], row['Drink'], row['Sides']))

# Insert orders into the database
for _, row in data.iterrows():
    # Check if the order already exists
    cursor.execute("SELECT COUNT(*) FROM orders WHERE order_id = %s", (row['Order ID'],))
    order_exists = cursor.fetchone()[0]
    
    if order_exists == 0:
        cursor.execute("""
            INSERT INTO orders (order_id, order_date, delivery_date, customer_id, cost, sales, quantity, discount, delivery_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (row['Order ID'], pd.to_datetime(row['Order Date'], dayfirst=True), pd.to_datetime(row['Delivery Date'], dayfirst=True), row['Customer ID'], row['Cost'], row['Sales'], row['Quantity'], row['Discount'], row['Delivery Cost']))

# Commit the transactions and close the connection
connection.commit()
cursor.close()
connection.close()

print("Data inserted successfully.")
