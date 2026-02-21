# 🖥 Computer Sales Service System

A complete **Console-Based Computer Sales Management System** built using **Python and MySQL**.

This project manages computer inventory, handles customer purchases, generates invoices, maintains transaction records, and produces sales reports — all through a structured menu-driven interface.

---

## 🚀 Features

### 📦 Inventory Management
- Add new computers
- View available computers
- Update computer price & stock
- Delete computers safely
- Automatic ID renumbering

### 🛒 Sales & Checkout System
- Purchase computers
- Real-time stock validation
- Automatic stock deduction
- Customer information capture
- Invoice generation

### 📊 Reporting & Analytics
- Sales report generation
- Transaction history tracking
- Total stock value calculation
- Average price calculation
- Low stock alerts

### 🧾 Invoice Generation
- Displays formatted invoice
- Includes:
  - Customer details
  - Purchase date
  - Product details
  - Quantity
  - Total price

### 🔁 Data Integrity
- Transaction ID renumbering
- Referential handling before deletion
- Automatic database and table creation

---

## 🛠 Technologies Used

- Python 3
- MySQL
- mysql-connector-python
- PrettyTable
- datetime (built-in)

---

## 🗄 Database Structure

### Database Name:
```
ComputerSalesDB
```

### Tables:

#### 1️⃣ computers
- id (Primary Key)
- brand
- model
- price
- stock

#### 2️⃣ transactions
- id (Primary Key)
- computer_id
- quantity
- total_price
- date_time
- customer_name
- customer_address
- customer_email

---

## 📂 Project Structure

```
Computer_Sales_Service_System/
│
├── appf.py
├── README.md
└── (optional project documentation PDF)
```

---

## ⚙️ How to Run

### 1️⃣ Install Dependencies

```
pip install mysql-connector-python
pip install prettytable
```

---

### 2️⃣ Setup MySQL

Make sure:
- MySQL Server is installed
- MySQL is running
- You know your root password

---

### 3️⃣ Configure Database Password

Inside the file:

```
password="YOUR_MYSQL_PASSWORD"
```

Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL password.

⚠ Do NOT upload your real password publicly.

---

### 4️⃣ Run the Program

```
python appf.py
```

The program will automatically:
- Create the database (if not exists)
- Create required tables
- Start the main menu

---

## 🖥 Main Menu Options

1. Add Computer  
2. View Computers  
3. Update Computer  
4. Delete Computer  
5. View Current Statistics  
6. Checkout  
7. Sales Report  
8. Delete Transaction  
9. Stock Alert  
10. Exit  

---

## 📊 Example Capabilities

✔ Automatic invoice generation  
✔ Formatted tables using PrettyTable  
✔ Stock availability validation  
✔ Sales tracking with customer details  
✔ Low-stock monitoring  

---

## 💡 Future Improvements

- Implement user authentication system
- Add role-based access (Admin/Staff)
- Export reports to PDF/Excel
- Add GUI using Tkinter or PyQt
- Use environment variables for database credentials
- Add proper foreign key constraints

---

## 🔐 Security Note

For better security, avoid hardcoding your MySQL password.

Instead, use environment variables:

```python
import os
password = os.getenv("MYSQL_PASSWORD")
```

Then set it in your system environment.

---

## 👨‍💻 Author

Anubhav Arya  
Python Developer | Database & Backend Enthusiast

---

## 📌 Project Type

Academic / Database Management System Project  
Console-Based Management Software
