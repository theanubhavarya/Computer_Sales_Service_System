import mysql.connector
from mysql.connector import Error  # For better error handling
from prettytable import PrettyTable  # Importing PrettyTable for table display
import datetime

# Initial connection setup without specifying a database
def get_connection_initial():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD"
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        exit(1)


# Connection setup with a specific database
def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD",
            database="ComputerSalesDB"
        )
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        exit(1)


# Function to create the database if it doesn't exist
def create_database():
    connection = get_connection_initial()
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ComputerSalesDB")
    print("Database 'ComputerSalesDB' is ready.")
    cursor.close()
    connection.close()


# Function to create the table if it doesn't exist
def create_table():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS computers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            brand VARCHAR(50),
            model VARCHAR(50),
            price DECIMAL(10, 2),
            stock INT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            computer_id INT,
            quantity INT,
            total_price DECIMAL(10, 2),
            date_time DATETIME,
            customer_name VARCHAR(100),
            customer_address VARCHAR(255),
            customer_email VARCHAR(100)
        )
    """)
    print("Tables are ready.")
    cursor.close()
    connection.close()


# Function to renumber IDs and reset AUTO_INCREMENT
def renumber_ids():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SET @new_id = 0")
    cursor.execute("UPDATE computers SET id = (@new_id := @new_id + 1) ORDER BY id")
    connection.commit()
    print("IDs have been renumbered.")
    cursor.close()
    connection.close()


# Add a new computer record
def add_computer(brand, model, price, stock):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO computers (brand, model, price, stock) VALUES (%s, %s, %s, %s)"
    values = (brand, model, price, stock)
    cursor.execute(query, values)
    connection.commit()
    print("Computer added successfully.")
    cursor.close()
    connection.close()
    renumber_ids()


# View all computer records in a table format
def view_computers():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM computers")
    results = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["ID", "Brand", "Model", "Price", "Stock"]
    
    # Format price with the $ symbol
    for row in results:
        row_with_price = list(row)  # Make a copy of the row
        row_with_price[3] = f"${row_with_price[3]:,.2f}"  # Format the price with $ and commas
        table.add_row(row_with_price)
    
    print(table)
    cursor.close()
    connection.close()


# Update a computer record
def update_computer(id, price, stock):
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE computers SET price = %s, stock = %s WHERE id = %s"
    values = (price, stock, id)
    cursor.execute(query, values)
    connection.commit()
    print("Computer updated successfully.")
    cursor.close()
    connection.close()


# Delete a computer record
def delete_computer(id):
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Step 1: Update all transactions with this computer's ID to NULL to maintain referential integrity
        cursor.execute("UPDATE transactions SET computer_id = NULL WHERE computer_id = %s", (id,))
        connection.commit()

        # Step 2: Delete the computer from the computers table
        cursor.execute("DELETE FROM computers WHERE id = %s", (id,))
        connection.commit()

        # Step 3: Renumber IDs in the computers table (safe)
        renumber_ids()

        # Step 4: Renumber transaction IDs to maintain consistency
        renumber_transaction_ids()

        print(f"Computer with ID {id} deleted and IDs renumbered successfully.")

    except Exception as e:
        print(f"Error deleting computer: {e}")
    finally:
        if connection:
            connection.close()


# Get current statistics
def get_statistics():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM computers")
    total_computers = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(price * stock) FROM computers")
    total_value = cursor.fetchone()[0] or 0
    cursor.execute("SELECT AVG(price) FROM computers")
    average_price = cursor.fetchone()[0] or 0

    # Create PrettyTable to display the statistics
    table = PrettyTable()
    table.field_names = ["Statistic", "Value"]
    
    # Format total_value and average_price with $ symbol and commas
    formatted_total_value = f"${total_value:,.2f}"  # Add $ symbol and format total stock value with commas and 2 decimal places
    formatted_average_price = f"${average_price:,.2f}"  # Add $ symbol and format average price with commas and 2 decimal places
    
    table.add_row(["Total Computers", total_computers])
    table.add_row(["Total Stock Value", formatted_total_value])
    table.add_row(["Average Price", formatted_average_price])

    # Print the table
    print(table)

    cursor.close()
    connection.close()


# Generate and print the invoice
def generate_invoice(computer_id, quantity, total_price, customer_name, customer_address, customer_email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT brand, model FROM computers WHERE id = %s", (computer_id,))
    computer = cursor.fetchone()
    if not computer:
        print("Invalid computer ID.")
        return
    brand, model = computer
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table = PrettyTable()
    table.field_names = ["Invoice Details", "Information"]
    table.add_row(["Invoice Date", date_time])
    table.add_row(["Customer Name", customer_name])
    table.add_row(["Customer Address", customer_address])
    table.add_row(["Customer Email", customer_email or "N/A"])
    table.add_row(["Brand", brand])
    table.add_row(["Model", model])
    table.add_row(["Quantity", quantity])
    table.add_row(["Total Price", f"₹{total_price:.2f}"])
    print("\n" + "=" * 40)
    print(f"INVOICE - Purchase Date: {date_time}")
    print(table)
    print("=" * 40)
    print("Thank you for your purchase!")
    print("=" * 40)
    cursor.close()
    connection.close()


# Checkout process
def checkout():
    connection = get_connection()
    cursor = connection.cursor()
    view_computers()
    try:
        computer_id = int(input("Enter the ID of the computer you want to purchase: "))
        quantity = int(input("Enter quantity: "))
        cursor.execute("SELECT price, stock FROM computers WHERE id = %s", (computer_id,))
        result = cursor.fetchone()
        if not result:
            print("Invalid computer ID.")
            return
        price, stock = result
        if quantity > stock:
            print("Insufficient stock available.")
            return
        total_price = price * quantity
        confirmation = input(f"Total price is ₹{total_price:.2f}. Confirm purchase? (yes/no): ").strip().lower()
        if confirmation != "yes":
            print("Purchase cancelled.")
            return
        customer_name = input("Name: ").strip()
        customer_address = input("Address: ").strip()
        customer_email = input("Email (optional): ").strip()
        if not customer_name or not customer_address:
            print("Name and address cannot be empty.")
            return
        cursor.execute("UPDATE computers SET stock = stock - %s WHERE id = %s", (quantity, computer_id))
        cursor.execute("""
            INSERT INTO transactions (computer_id, quantity, total_price, date_time, customer_name, customer_address, customer_email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (computer_id, quantity, total_price, datetime.datetime.now(), customer_name, customer_address, customer_email))
        connection.commit()
        print("Purchase successful! Generating invoice...")
        generate_invoice(computer_id, quantity, total_price, customer_name, customer_address, customer_email)
    except ValueError:
        print("Invalid input. Please enter numeric values for IDs and quantities.")
    finally:
        cursor.close()
        connection.close()


def sales_report():
    try:
        print("Generating sales report...")  # Debugging line

        # Renumber transaction IDs before generating the report
        renumber_transaction_ids()

        connection = get_connection()
        cursor = connection.cursor()

        # Fetch transactions with related computer details and customer info (address & email)
        cursor.execute("""
            SELECT 
                t.id, c.brand, c.model, t.quantity, t.total_price, t.date_time, t.customer_name, 
                t.customer_address, t.customer_email
            FROM transactions t
            INNER JOIN computers c ON t.computer_id = c.id
        """)
        rows = cursor.fetchall()

        # Print the report using PrettyTable
        table = PrettyTable()
        table.field_names = ["Transaction ID", "Brand", "Model", "Quantity", "Total Price", "Date & Time", "Customer Name", "Customer Address", "Customer Email"]

        for row in rows:
            # Format the total_price with $ symbol and proper number formatting
            formatted_price = f"${row[4]:,.2f}"  # Add $ symbol and format the price with commas and 2 decimal places
            row_with_price = list(row)  # Convert tuple to list to modify the price
            row_with_price[4] = formatted_price  # Replace the total price with the formatted price

            table.add_row(row_with_price)

        print(table)

        cursor.close()
        connection.close()

        print("Sales report generated. Returning to main menu...")  # Debugging line
        return  # Explicit return to exit sales_report() and return to main()

    except Exception as e:
        print(f"Error generating sales report: {e}")
        if connection:
            connection.close()  # Ensure connection is closed on error
        return  # Ensure function exits on error


def delete_transaction(transaction_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Deleting the transaction based on the given transaction ID
        query = "DELETE FROM transactions WHERE id = %s"
        cursor.execute(query, (transaction_id,))
        connection.commit()

        print(f"Transaction with ID {transaction_id} deleted successfully.")

        # Renumber transaction IDs after deletion
        renumber_transaction_ids()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        if connection:
            connection.close()


# Function to renumber transaction IDs and reset AUTO_INCREMENT
def renumber_transaction_ids():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Step 1: Renumber transaction IDs
        cursor.execute("SET @new_id = 0")
        cursor.execute("UPDATE transactions SET id = (@new_id := @new_id + 1) ORDER BY id")
        
        # Step 2: Reset AUTO_INCREMENT to the next available ID (renumbering continuity)
        cursor.execute("ALTER TABLE transactions AUTO_INCREMENT = 1")
        connection.commit()

        print("Transaction IDs have been renumbered.")

    except Exception as e:
        print(f"Error renumbering transaction IDs: {e}")
    finally:
        cursor.close()
        connection.close()


# Low Stock alert
def stock_alert(threshold=5):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, brand, model, stock FROM computers WHERE stock < %s", (threshold,))
    rows = cursor.fetchall()
    if rows:
        print("Low stock alert:")
        table = PrettyTable()
        table.field_names = ["ID", "Brand", "Model", "Stock"]
        for row in rows:
            table.add_row(row)
        print(table)
    else:
        print("All items are well-stocked.")

    cursor.close()
    connection.close()


# Main menu
def main():
    create_database()
    create_table()
    while True:

        print("\n" + "Computer Sales Management System".center(50, "-"))
        print("1. Add Computer")
        print("2. View Computers")
        print("3. Update Computer")
        print("4. Delete Computer")
        print("5. View Current Statistics")
        print("6. Checkout")
        print("7. Sales Report")
        print("8. Delete Transaction")
        print("9. Stock Alert")
        print("10. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            brand = input("Enter brand: ")
            model = input("Enter model: ")
            try:
                price = float(input("Enter price: "))
                stock = int(input("Enter stock: "))
                add_computer(brand, model, price, stock)
            except ValueError:
                print("Invalid input! Price must be a number, and stock must be an integer.")
        elif choice == "2":
            view_computers()
        elif choice == "3":
            try:
                id = int(input("Enter computer ID to update: "))
                price = float(input("Enter new price: "))
                stock = int(input("Enter new stock: "))
                update_computer(id, price, stock)
            except ValueError:
                print("Invalid input! Please enter valid numbers.")
        elif choice == "4":
            try:
                id = int(input("Enter computer ID to delete: "))
                delete_computer(id)
            except ValueError:
                print("Invalid input! ID must be an integer.")
        elif choice == "5":
            get_statistics()
        elif choice == "6":
            checkout()
        elif choice == "7":
            sales_report()
        elif choice == "8":
            try:
                transaction_id = int(input("Enter transaction ID to delete: "))  # Get transaction ID to delete
                delete_transaction(transaction_id)
            except ValueError:
                print("Invalid input! Transaction ID must be an integer.")
        elif choice == "9":
            stock_alert()
        elif choice == "10":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()




