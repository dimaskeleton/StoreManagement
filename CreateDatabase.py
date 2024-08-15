# Needed libraries
import sqlite3

# ONLY NEEDS TO BE RUN ONCE IF THE DATABASE DOESN'T ALREADY, ONLY INITIALIZES IT AND DOESN'T FILL WITH DATA

'''
Purpose: Create a new database for a grocery store with tables for products, sales, and customers 
         with each one having it's own table and data 
'''


def create_database():
    connection = sqlite3.connect('shop.db')  # Creates a connection to 'shop.db'
    cursor = connection.cursor()  # Creates a cursor

    # Creates a table for products if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        )''')

    # Create the customers table if it doesn't already exist
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT,
                contact TEXT
            )''')

    # Create the sales table with a foreign key to reference products and customers tables if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            customer_id INTEGER,
            quantity INTEGER,
            date TEXT,
            FOREIGN KEY (product_id) REFERENCES products (product_id),
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )''')

    connection.commit()
    connection.close()


# Same function as defined earlier just redefined to create a TESTshop.db for testing all the methods
def create_test_database():
    connection = sqlite3.connect('TESTshop.db')
    cursor = connection.cursor()
    # Create the products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        )''')

    # Create the sales table with a foreign key to customers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            customer_id INTEGER,
            quantity INTEGER,
            date TEXT,
            FOREIGN KEY (product_id) REFERENCES products (product_id),
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )''')

    # Create the customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            contact TEXT
        )''')

    connection.commit()
    connection.close()

# Calls and creates the databases (Commented out since they are already created)
# create_database()
# create_test_database()
