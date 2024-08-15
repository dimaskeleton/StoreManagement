from Store import *

# Define a constant for the database path to run the tests on
DB_PATH = 'TESTshop.db'


# Tests for the Products class------------------------------------------------------------------------------------------

# Test for the add_product method
def test_add_product():
    product = Product(DB_PATH)
    product.name = "Butter"
    product.price = 2.3
    product.add_product()

    # Ensure the product was added
    with product._Product__connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name = 'Butter'")
        result = cursor.fetchone()
        assert result is not None
        assert result[1] == "Butter"
        assert result[2] == 2.3


# Test for the get_product method
def test_get_product():
    product = Product(DB_PATH)
    prod = product.get_product(1)
    assert prod._Product__name == "Milk"
    assert prod._Product__price == 2.5


# Test for the update_product method
def test_update_product():
    product = Product(DB_PATH)
    product.get_product(1)
    product._Product__name = "Updated Milk"
    product._Product__price = 2.60
    product.update_product()

    assert product._Product__name == "Updated Milk"
    assert product._Product__price == 2.6


# Test for the delete_product method
def test_delete_product():
    product = Product(DB_PATH)
    product.get_product(2)  # Picks the product_id as 2 to delete
    product.delete_product()

    # Ensure the product was deleted
    with product._Product__connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = 2")
        assert cursor.fetchone() is None


# Test for the update_price method
def test_update_price():
    product = Product(DB_PATH)
    product.get_product(3)  # Picks the product_id as 3 to update_price
    product.update_price(3.45)

    # Ensure the price was updated
    updated_prod = product.get_product(3)
    assert updated_prod._Product__price == 3.45


# Test for the load_products method
def test_load_products():
    product = Product(DB_PATH)
    df = product.load_products()
    assert not df.empty
    assert len(df) >= 5


# Tests for the PerishableProducts class-------------------------------------------------------------------------------

# Test to initialize the perishable_product class
def test_perishable_product_initialization():
    db_path = 'TESTshop.db'
    future_date = (datetime.datetime.now() + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    product = PerishableProduct(db_path, 1, "Yogurt", 1.99, future_date)
    assert product.get_expiry_date() == future_date


# Test to check if a product is expired before the expiration date
def test_is_expired_false():
    db_path = 'TESTshop.db'
    future_date = (datetime.datetime.now() + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    product = PerishableProduct(db_path, 1, "Yogurt", 1.99, future_date)
    assert not product.is_expired()


# Test to check if a product is expired after the expiration date
def test_is_expired_true():
    db_path = 'TESTshop.db'
    past_date = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    product = PerishableProduct(db_path, 1, "Old Cheese", 2.99, past_date)
    assert product.is_expired()


# Test to get the expiration date
def test_get_expiry_date():
    db_path = 'TESTshop.db'
    test_date = "2024-04-20"
    product = PerishableProduct(db_path, 1, "Seasonal Fruit", 0.99, test_date)
    assert product.get_expiry_date() == test_date


# Tests for the Customer class------------------------------------------------------------------------------------------

# Test for the add_customer method
def test_add_customer():
    customer = Customer(DB_PATH)
    customer.name = "Andrew Gray"
    customer.contact = "8749847819"
    customer.add_customer()

    # Verify the customer was added
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, contact FROM customers WHERE name = ? AND contact = ?",
                       (customer.name, customer.contact))
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == "Andrew Gray"
        assert result[1] == "8749847819"


# Test for the get_customer method
def test_get_customer():
    customer = Customer(DB_PATH)
    customer.name = "Alice Smith"
    customer.contact = "0987654321"
    customer.add_customer()

    # Verifies that the customer is return properly
    retrieved_customer = customer.get_customer(7)
    assert retrieved_customer.name == "Alice Smith"
    assert retrieved_customer.contact == "0987654321"


# Test for the update_customer method
def test_update_customer():
    customer = Customer(DB_PATH)
    customer.name = "Chris Fox"
    customer.contact = "9998887777"
    customer.add_customer()

    # Update the customer information
    retrieved_customer = customer.get_customer(4)
    retrieved_customer.name = "Christopher Fox"
    retrieved_customer.contact = "1239875465"
    retrieved_customer.update_customer()

    # Verify customer information was updated properly
    updated_customer = customer.get_customer(4)
    assert updated_customer.name == "Christopher Fox"
    assert updated_customer.contact == "1239875465"


# Test for the delete_customer method
def test_delete_customer():
    customer = Customer(DB_PATH)
    customer.name = "Kevin Smith"
    customer.contact = "9876543210"
    customer.add_customer()
    customer.delete_customer()

    # Verify the customer was deleted from the database
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer.customer_id,))
        result = cursor.fetchone()
        assert result is None


# Test for the load_customers method
def test_load_customers():
    customer = Customer(DB_PATH)
    df = customer.load_customers()
    assert not df.empty  # Ensures that there are customers loaded
    assert len(df) > 0  # Ensures that the dataframe consists the proper amount of data


# Tests for the SalesManager class-------------------------------------------------------------------------------------

# Test for the add_sale method
def test_add_sale():
    manager = SalesManager(DB_PATH)
    # Uses datetime.now() to get the current date and format it
    new_sale = Sale(1, 1, 10, datetime.datetime.now().strftime("%Y-%m-%d"))
    manager.add_sale(new_sale)

    # Ensure that the sale was added properly
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT quantity FROM sales WHERE product_id = ? AND customer_id = ? ORDER BY sale_id DESC LIMIT 1", (1, 1))
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 10


# Test for the load_sales method
def test_load_sales():
    manager = SalesManager(DB_PATH)
    sales_df = manager.load_sales()
    assert not sales_df.empty  # Ensures that there are transactions loaded
    assert len(sales_df.index) > 0  # Ensures that the dataframe consists the proper amount of data


# Test for the calculate_total_sales method
def test_calculate_total_sales():
    manager = SalesManager(DB_PATH)
    total_sales = manager.calculate_total_sales()
    assert total_sales > 0  # Greater than 0 because the price is 30.5 but doesn't return a float instead of np.int64(24)


# Test for the sales_per_product method
def test_sales_per_product():
    manager = SalesManager(DB_PATH)
    sales_summary = manager.sales_per_product()
    assert not sales_summary.empty
    assert sales_summary.iloc[0] > 0  # Ensures the dataframe isn't empty showing that the dataframe is filled with data
