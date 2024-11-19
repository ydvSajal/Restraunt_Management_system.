# Restraunt_Management_system.
Basic restaurant management system (RMS) using pyhton and java 
# Restaurant Management System

This is a simple Restaurant Management System implemented in Python. It allows users to view the menu, place orders, review items, and view transaction history. Additionally, administrators can update the menu and add new items.

## File Structure

- **data/menu.json**: Contains the menu data.
- **data/admins.json**: Stores admin credentials.
- **data/transactions.json**: Records transaction history.

## Prerequisites

Before understanding the code, it is recommended to have knowledge of the following:

- **Basic Python**: Familiarity with Python syntax and basic concepts.
- **JSON Handling**: Understanding how to read and write data to JSON files.
- **Datetime Module**: Knowledge of the `datetime` module for handling timestamps.
- **List Comprehensions**: Understanding the use of list comprehensions, especially in the context of searching through lists.

## Key Functions

### 1. `show_menu`

Displays the restaurant menu with details like item ID, name, price, and average rating.

### 2. `order_items`

Allows users to place orders by selecting items from the menu, specifying the quantity, and confirming the order.

### 3. `review_item`

Enables users to review items by providing a rating (1-5).

### 4. `update_menu`

For administrators only. Allows admins to update the price of an item in the menu.

### 5. `add_new_product`

For administrators only. Enables admins to add new items to the menu.

### 6. `show_transactions`

Displays a table of past transactions, including details like item name, quantity, total price, and timestamp.

### 7. `exit_program`

Exits the Restaurant Management System.

Feel free to explore and modify the code based on your requirements!

## Usage
1. Choose options from the main menu (1-7) to perform various tasks.
2. For admin-related tasks, provide valid admin credentials.

## Notes
- Ensure that you have the necessary permissions to modify data files.
- Admin credentials are stored in `data/admins.json`. Ensure the credentials are correct for admin functionalities.
- 
Feel free to explore, modify, and enhance the code as needed!
