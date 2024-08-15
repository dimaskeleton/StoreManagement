# Needed libraries
from Store import *
import random
from datetime import timedelta, datetime

'''
Purpose: To fill the shop.db database with data for products, customers, and sales to represent what a real store 
         database may look like 
         
Contract: fill_products(): Fills the products table with a defined list of products
          fill_customers(): Fills the customer table with a defined list of customers
          fill_sales(): # Fills the sales table with a defined, randomly generated list of transactions
          random_date(): Creates a random date within a given range use for sales_data
'''


# Fills the shop database, product table with the following list of products with their price:
def fill_products(db_path):
    products = [
        ("Apple", 0.50),
        ("Banana", 0.30),
        ("Orange", 0.40),
        ("Milk", 1.50),
        ("Bread", 1.20),
        ("Cheese", 2.50),
        ("Yogurt", 0.99),
        ("Chicken", 5.00),
        ("Beef", 7.50),
        ("Pork", 5.90),
        ("Salmon", 6.25),
        ("Lettuce", 1.10),
        ("Tomato", 0.75),
        ("Potato", 0.45),
        ("Onion", 0.60),
        ("Pepper", 1.00),
        ("Ice Cream", 2.00),
        ("Candy", 1.50),
        ("Cereal", 2.50),
        ("Oatmeal", 3.00),
        ("Rice", 0.50),
        ("Cookies", 5.00),
        ("Chips", 1.00),
        ("Flavored Chips", 1.50),
        ("Sandwhich", 10.00),
        ("Cold Cuts", 4.00),
    ]
    for name, price in products:
        product = Product(db_path=db_path)
        product.name = name
        product.price = price
        product.add_product()


# Fills the shop database, customer table with the following list of customers with their phone number:
def fill_customers(db_path):
    customers = [
        ("Robyn Ford", "2015543721"),
        ("Sallie Boyer", "987654321"),
        ("Fern Kane", "9738129053"),
        ("Duane Donovan", "8912345678"),
        ("Dallas Morris", "2019987745"),
        ("Rita Clark", "9733238821"),
        ("Saul Walsh", "8917864321"),
        ("Sheldon Compton", "2014679912"),
        ("Leanna Bradford", "9734106643"),
        ("Deon Campbell", "8911234567"),
        ("Markus Rojas", "2012759098"),
        ("Hilario Cline", "9735006214"),
        ("Carlos Monroe", "8915647890"),
        ("Sharlene Waller", "2018347756"),
        ("Trent Jarvis", "9732913354"),
        ("Lynne Moore", "8919876543"),
        ("Millard Cardenas", "2015422289"),
        ("Sadie Benjamin", "9734440987"),
        ("Nelson Stevens", "8913210987"),
        ("Julius Gross", "2016018899"),
        ("Chloe Long", "9738235661")
    ]
    for name, contact in customers:
        customer = Customer(db_path=db_path)
        customer.name = name
        customer.contact = contact
        customer.add_customer()


# Creates a random date between certain dates already defined
def random_date(start, end):
    delta = end - start  # start is the start date and end is the end date (giving the range for the dates)
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)  # Gets a random second
    return start + timedelta(seconds=random_second)  # Returns the random datetime to fill sales


# Fills the shop database, sales table randomly with the following list
# of sales with their customer_id, amount of what on this day
def fill_sales(db_path):
    start_date = datetime.strptime("2024-04-01", "%Y-%m-%d")
    end_date = datetime.strptime("2024-04-30", "%Y-%m-%d")

    customers = range(1, 22)  # IDs for 21 customers
    products = range(1, 27)  # IDs for 26 products
    sales_manager = SalesManager(db_path=db_path)  # Sets the db_path
    sales = []  # List of sales transactions

    for _ in range(100):  # Generate 100 transactions
        customer_id = random.choice(list(customers))  # Picks a random customer
        product_id = random.choice(list(products))  # Picks a random product
        quantity = random.randint(1, 15)  # Picks a random amount between 1 and 15
        date = random_date(start_date, end_date).strftime("%Y-%m-%d")  # Picks a random date between start/end time
        sales.append(Sale(product_id, customer_id, quantity, date))  # Adds the transaction to the list

    # Iterates through sales list adding each transaction to the database 
    for sale in sales:
        sales_manager.add_sale(sale)


# Same methods as earlier to fill a database with predefined data but condensed and simplified to test all methods in
# Store.py to ensure it's all working as expected


# Fills the test database with products
def test_populate_products(db_path):
    products = [
        ("Milk", 2.50),
        ("Strawberry", 0.30),
        ("Ice Cream", 3.40),
        ("Mozzarella", 1.50),
        ("Cereal", 1.20)
    ]
    product_manager = Product(db_path)
    for name, price in products:
        product_manager.name = name
        product_manager.price = price
        product_manager.add_product()


# Fills the test database with customers
def test_populate_customers(db_path):
    customers = [
        ("Alex Jones", "1234567890"),
        ("Kevin Smith", "9876543210"),
        ("David Kendall", "1112223333"),
        ("Chris Fox", "9998887777"),
        ("Brianna Molleen", "5553338888")
    ]
    customer_manager = Customer(db_path)
    for name, contact in customers:
        customer_manager.name = name
        customer_manager.contact = contact
        customer_manager.add_customer()


# Fills the test database with sales (not randomly generated)
def test_populate_sales(db_path):
    sales = [
        (1, 7, 3, "2024-04-15"),
        (2, 5, 1, "2024-04-16"),
        (5, 2, 5, "2024-04-16"),
        (1, 9, 2, "2024-04-17"),
        (3, 4, 3, "2024-04-18")
    ]
    sales_manager = SalesManager(db_path)
    for product_id, customer_id, quantity, date in sales:
        sale = Sale(product_id=product_id, customer_id=customer_id, quantity=quantity, date=date)
        sales_manager.add_sale(sale)


# Main function to run and fill the databases with the predefined data
# Incorporates both the main and test methods defined earlier, in order to run
# either one just uncomment/comment the block below
if __name__ == "__main__":
    '''
    # For the main 'shop.db' database 
    db_path = 'shop.db'
    fill_products(db_path)
    fill_customers(db_path)
    fill_sales(db_path)
    '''

    # For the testing database
    db_path = 'TESTshop.db'
    test_populate_products(db_path)
    test_populate_customers(db_path)
    test_populate_sales(db_path)
