# Needed libraries
import sqlite3
import datetime
import pandas as pd
import matplotlib.pyplot as plt

'''
Purpose: Manages products in a database for a grocery store consisting of functions for CRUD operations on the products
         and functions to generate visual plots based on the product data stored in the database 

Contact: add_product(): Adds a product to the database with it's name and price 
         get_product(): Gets and returns the given product information such as name and price 
         update_product(): Updates the products to whatever is given to it 
         delete_product(): Removes a product from the database 
         update_price(): Sets a new updated price for the product updating the database  
         load_products(): Gets all the products and returns them as a dataframe 
         plot_product_prices(): Creates a bar chart of all products and their prices
         plot_sales_by_product(): Creates a bar chart displaying total sales amount by product
         
'''


class Product:
    # Initializes product class with path to the database
    def __init__(self, db_path):
        self.db_path = db_path  # Initializes database path
        self.product_id = None  # Initializes product_id
        self.name = None  # Initializes product name being private
        self.price = None  # Initializes product price being private

    # Create a connection to the database
    def __connect(self):
        return sqlite3.connect(self.db_path)  # Returns the connection

    # Adds a product to the database
    def add_product(self):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Executes command to add the product to the database
            cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', (self.name, self.price))
            conn.commit()  # Commits the changes

    # Gets a product based on the product_id from the database and updated the initialized variables
    def get_product(self, product_id):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Gets the columns of product_id that matches
            cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
            row = cursor.fetchone()  # Gets the first row of the results after cursor execution
            # Checks if any row exists/retrieved
            if row:
                self.product_id, self.__name, self.__price = row  # If row exists set the product data to self attributes
                return self  # Returns the product data retrieved from the database
            return None  # If product doesn't exist, return nothing

    # Updates the details of a product in the database
    def update_product(self):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Executes command to update a product details in the database
            cursor.execute('UPDATE products SET name = ?, price = ? WHERE product_id = ?',
                           (self.__name, self.__price, self.product_id))
            conn.commit()  # Commits the changes to the database

    # Deletes a product based on the product_id from the database
    def delete_product(self):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Executes command to delete the product from the database
            cursor.execute('DELETE FROM products WHERE product_id = ?', (self.product_id,))
            conn.commit()  # Commits the changes to the database

    # Sets a new price for the product in the database
    def update_price(self, new_price):
        # Ensures that the new_price is greater than 0 since price can't be negative
        if new_price > 0:
            self.__price = new_price  # Sets the price to the new price
            self.update_product()  # Updates the product with the new price
        else:
            raise ValueError("New price must be positive")  # Raises an error if the given price is negative

    # Gets all the products from the database and returns them as a dataframe
    def load_products(self):
        with self.__connect() as conn:
            return pd.read_sql('SELECT * FROM products', conn)

    # Plots a bar chart of the products with their prices
    def plot_product_prices(self):
        with self.__connect() as conn:
            # Gets the products and creates a dataframe from them
            df = pd.read_sql_query('SELECT name, price FROM products', conn)

        plt.figure(figsize=(8, 5))  # Sets the figure size
        plt.bar(df['name'], df['price'],
                color='blue')  # Gets the name and price of the products to plot with color blue
        plt.xlabel('Product')  # Sets the X axis to 'Product'
        plt.ylabel('Price ($)')  # Sets the Y axis to 'Price ($)'
        plt.title('Price Across Products')  # Sets the title of the chart to 'Price Across Products'
        plt.xticks(rotation=90)  # Sets X axis labels rotated to 90º
        plt.show()  # Displays the chart

    # Plots a bar chart showing the total sales amount by product
    def plot_sales_by_product(self):
        with self.__connect() as conn:
            # Gets the products and sum of the amount sold, joining the tables giving each product sum its own ID
            # Ordering it from highest to lowest putting it in the dataframe to plot
            query = '''
            SELECT p.name, SUM(s.quantity) AS total_sold
            FROM products p JOIN sales s ON p.product_id = s.product_id
            GROUP BY p.product_id
            ORDER BY total_sold DESC
            '''
            df = pd.read_sql_query(query, conn)

        plt.figure(figsize=(10, 6))  # Sets the figure size
        plt.bar(df['name'], df['total_sold'],
                color='purple')  # Gets the name and total_sold from the dataframe plotting them purple
        plt.xlabel('Product')  # Sets the X axis to 'Product'
        plt.ylabel('Total Amount Sold')  # Sets the Y axis to 'Total Amount Sold'
        plt.title('Total Sales by Products')  # Sets the title of the chart to 'Total Sales by Products'
        plt.xticks(rotation=90)  # Sets X axis labels rotated to 90º
        plt.show()  # Displays the chart


'''
Purpose: Extends the Product class to manage perishable products separating from the main products with features such as 
         having expiration dates and seeing what products are expired 
         
Contract: is_expired(): Returns True or False whether the product is expired or not 
          get_expiry_date(): Returns the expiration date in Y-M-D format 
'''


class PerishableProduct(Product):
    # Initializes PerishableProduct class with specific variables for perishable products
    def __init__(self, db_path, product_id, name, price, expiry_date):
        super().__init__(db_path)  # Calls db_path from already initialized in the Product class
        self.product_id = product_id  # Initializes product_id
        self.name = name  # Initializes the product's name
        self.price = price  # Initializes the product price
        self.__expiry_date = datetime.datetime.strptime(expiry_date, "%Y-%m-%d")  # Converts expiry date to dt format

    # Checks if the product is expired
    def is_expired(self):
        # Compares the current date to the expiration date return True or False
        return self.__expiry_date < datetime.datetime.now()

    # Returns the expiration date of the product in Y-M-D format
    def get_expiry_date(self):
        return self.__expiry_date.strftime("%Y-%m-%d")  # Returns the expiration date


'''
Purpose: Manages customers in the customer database consisting of functions to add, get, update, delete customer data
         from the database 
         
Contract: add_customer(): Adds a new customer to the database with their name and contact information
          get_customer(): Gets and returns customer info based on the customer_id 
          update_customer(): Update's customer info in the database from the customer_id 
          delete_customer(): Deletes a customer from the database from the customer_id 
          load_customers(): Loads and returns all the customer's and their info from the database 
          plot_customer_contact_distribution(): Creates a bar chart of customer's and their area code 
'''


class Customer:
    # Initializes customer class with path to the database
    def __init__(self, db_path):
        self.db_path = db_path  # Initializes database path
        self.customer_id = None  # Initializes customer_id
        self.name = None  # Initializes customer name
        self.contact = None  # Initializes customer contact info

    # Create a connection to the database
    def __connect(self):
        return sqlite3.connect(self.db_path)

    # Adds a customer to the database
    def add_customer(self):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Executes command to add a new customer to the database
            cursor.execute('INSERT INTO customers (name, contact) VALUES (?, ?)', (self.name, self.contact))
            conn.commit()  # Commits the changes to the database

    # Returns a customer from the database based on the customer_id
    def get_customer(self, customer_id):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Executes command to return a customer by customer_id from the database
            cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,))
            row = cursor.fetchone()
            if row:
                self.customer_id, self.name, self.contact = row  # Sets the attributes to the customer data
                return self  # Returns the customer with their data

    # Updates a customer's information in the database
    def update_customer(self):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Executes command to update a customer's information in the database
            cursor.execute('UPDATE customers SET name = ?, contact = ? WHERE customer_id = ?',
                           (self.name, self.contact, self.customer_id))
            conn.commit()  # Commits the changes to the database

    # Deletes a customer from the database based on the customer_id in the database
    def delete_customer(self):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Executes command to delete a customer from the database
            cursor.execute('DELETE FROM customers WHERE customer_id = ?', (self.customer_id,))
            conn.commit()  # Commits the changes to the database

    # Loads and returns all the customer and their data from the database
    def load_customers(self):
        with self.__connect() as conn:
            return pd.read_sql('SELECT * FROM customers', conn)  # Returns a dataframe with all the customers

    # Plots a distribution of customers by area code from their phone numbers
    def plot_customer_contact_distribution(self):
        with self.__connect() as conn:
            df = pd.read_sql_query('SELECT contact FROM customers', conn)  # Loads phone number data into a dataframe

            # Gets the area code from the contact, put it into a new column
            df['contact_region'] = df['contact'].apply(lambda x: x[:3])

        # Counts the occurrences of each area code from the customers
        contact_counts = df['contact_region'].value_counts()

        plt.figure(figsize=(8, 5))  # Sets the figure size
        contact_counts.plot(kind='bar')  # Creates a bar chart of the area code counts
        plt.xlabel('Area Code')  # Sets the X axis to 'Area Code'
        plt.ylabel('Frequency')  # Sets the Y axis to 'Frequency'
        plt.title('Customer Area Code Distribution')  # Sets the title of the chart to 'Customer Area Code Distribution'
        plt.show()  # Displays the chart


'''
Purpose: Manages sales and transactions in the database for the store consisting of functions to save, get, analyze sales
         data visualization, etc. 
         
Contract: add_sale(): Records and saves a transaction to the database 
          load_sales(): Loads and returns all the sales from the database 
          calculate_total_sales(): Adds and returns the total amount sold across all the transactions 
          sales_per_product(): Adds and returns the total sales organized by product 
          plot_sales_over_time(): Creates a line graph based on all the sales overtime 
          plot_sales_by_customer(): Creates a bar chart of sales organized by customer 
'''


class Sale:
    # Initializes Sale class with the following details:
    def __init__(self, product_id, customer_id, quantity, date):
        self.product_id = product_id  # Product ID with the sale
        self.customer_id = customer_id  # Customer ID with the sale
        self.quantity = quantity  # Quantity of the products sold
        self.date = date  # Date of the transaction


class SalesManager:

    # Initializes SalesManager class with path to the database
    def __init__(self, db_path):
        self.db_path = db_path  # Initializes database path

    # Creates a connection to the database
    def __connect(self):
        return sqlite3.connect(self.db_path)  # Returns the connection

    # Records a new sale in the database with details from the sale instance
    def add_sale(self, sale):
        with self.__connect() as conn:
            cursor = conn.cursor()  # Creates a cursor
            # Executes command to add the sale data to the database
            cursor.execute('INSERT INTO sales (product_id, customer_id, quantity, date) VALUES (?, ?, ?, ?)',
                           (sale.product_id, sale.customer_id, sale.quantity, sale.date))
            conn.commit()  # Commits the changes

    # Loads and returns all the sale data from the database
    def load_sales(self):
        with self.__connect() as conn:
            return pd.read_sql('SELECT * FROM sales', conn)  # Returns a dataframe with all the sales

    # Adds and returns the total quantity sold across all the transactions
    def calculate_total_sales(self):
        df = self.load_sales()  # Loads the sale data into a dataframe
        return df['quantity'].sum()  # Sums up the quantity column

    # Adds and returns total sales amount organized by product
    def sales_per_product(self):
        df = self.load_sales()  # Loads the sale data into a dataframe
        return df.groupby('product_id')['quantity'].sum()  # Groups by ID and sums quantities by the product

    # Plots a linechart of the sales amount over time
    def plot_sales_over_time(self):
        with self.__connect() as conn:
            # Loads the sale data into a dataframe
            df = pd.read_sql_query('SELECT date, sum(quantity) as total_quantity FROM sales GROUP BY date', conn)
            df['date'] = pd.to_datetime(df['date'])  # Converts date column to datetime format

        plt.figure(figsize=(10, 6))  # Sets the figure size
        plt.plot(df['date'], df['total_quantity'], color='green')  # Creates a green line chart of sales over date
        plt.xlabel('Date')  # Sets the X axis to 'Date'
        plt.ylabel('Total Amount Sold')  # Sets the Y axis to 'Total Amount Sold'
        plt.title('Total Sales Over Time')  # Sets the title of the chart to 'Total Sales Over Time'
        plt.show()  # Displays the chart

    # Plots a bar chart of sales amount organized by customer
    def plot_sales_by_customer(self):
        with self.__connect() as conn:
            # Gets customer names and sum of the products purchased by each one
            query = '''
            SELECT c.name, SUM(s.quantity) AS total_purchased
            FROM sales s JOIN customers c ON s.customer_id = c.customer_id
            GROUP BY s.customer_id
            ORDER BY total_purchased DESC
            '''
            df = pd.read_sql_query(query, conn)  # Sets the filtered data to a dataframe

        plt.figure(figsize=(10, 6))  # Sets the figure size
        plt.bar(df['name'], df['total_purchased'],
                color='cyan')  # Creates a cyan bar chart of name over total_purchased
        plt.xlabel('Customer Name')  # Sets the X axis to 'Customer Name'
        plt.ylabel('Total Amount Purchased')  # Sets the Y axis to 'Total Amount Purchased'
        plt.title('Total Sales by Customer')  # Sets the title of the chart to 'Total Sales by Customers'
        plt.xticks(rotation=90)  # Sets X axis labels rotated to 90º
        plt.show()  # Displays the chart


if __name__ == "__main__":
    db_path = 'shop.db'  # Define the path to the database

    # Initialize instances of each class with the database path
    product_manager = Product(db_path)
    customer_manager = Customer(db_path)
    sales_manager = SalesManager(db_path)

    # Puts products into a dataframe
    products_df = product_manager.load_products()
    print(products_df)  # Prints the products dataframe for visual confirmation

    # Puts customers into a dataframe
    customers_df = customer_manager.load_customers()
    print(customers_df)  # Prints the customers dataframe for visual confirmation

    # Puts sales into a dataframe
    sales_df = sales_manager.load_sales()
    print(sales_df)  # Prints he sales dataframe for visual confirmation

    # Calculates total sales using the calculate_total_sales method in SalesManager
    total_sales = sales_manager.calculate_total_sales()
    print(f"Total sales volume: {total_sales}")  # Prints the result

    # Calculates sales per product using sales_per_product method in SalesManager
    sales_per_product = sales_manager.sales_per_product()
    print("Sales per product:")
    print(sales_per_product)  # Prints the result

    # Plots all the methods for visualizations using the shop.db database
    # Product plots
    product_manager.plot_product_prices()
    product_manager.plot_sales_by_product()

    # Customer plot
    customer_manager.plot_customer_contact_distribution()

    # Sales plots
    sales_manager.plot_sales_over_time()
    sales_manager.plot_sales_by_customer()



