import json
import os
from datetime import datetime

class RestaurantManager:
    def __init__(self):
        # File paths for data storage
        self.menu_file = "data/menu.json"
        self.transactions_file = "data/transactions.json"
        self.admins_file = "data/admins.json"

        # Load initial data from files
        self.menu = self.load_data(self.menu_file)
        self.transactions = self.load_data(self.transactions_file)
        self.admins = self.load_data(self.admins_file)

    def load_data(self, file_name):
        # Load data from JSON file, return an empty list if the file doesn't exist
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                return json.load(file)
        return []

    def save_data(self, data, file_name):
        # Save data to JSON file with indentation for readability
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=2)

    # USER MENU
    
    def show_menu(self):
        # Display the menu in a tabular format with average rating
        print("\n{:<5} {:<25} {:<10} {:<10} {:<15}".format("ID", "Name", "Price ($)", "Veg", "Average Rating"))
        print("=" * 65)
        for item in self.menu:
            avg_rating = sum(item['reviews']) / len(item['reviews']) if item['reviews'] else 0
            print("{:<5} {:<25} {:<10.2f} {:<10} {:<15.2f}".format(item['id'], item['name'], item['price'], 'Veg' if item['veg'] else 'Non-Veg', avg_rating))
        print("=" * 65)
    
    def order_items(self):
        order_list = []
        
        while True:
            # Display menu and take order input
            self.show_menu()
            order_id = int(input("Enter the item ID you want to order: "))
            quantity = int(input("Enter the quantity: "))
            item = next((x for x in self.menu if x['id'] == order_id), None)

            if item:
                total_price = quantity * item['price']
                
                # Check if the item is already in the order list
                existing_order = next((order for order in order_list if order['item_id'] == order_id), None)
                if existing_order:
                    existing_order['quantity'] += quantity
                    existing_order['total_price'] += total_price
                    print(f"Added {quantity} {item['name']} to your existing order.")
                else:
                    order_list.append({"item_id": order_id, "quantity": quantity, "total_price": total_price, "name": item['name']})
                    print(f"Added {quantity} {item['name']} to your order.")
                
                # Display the current order
                print("\nCurrent Order:")
                for order in order_list:
                    print(f"{order['quantity']} {order['name']} - Total: ${order['total_price']}")
                
                # Ask if the user wants to add more items
                add_more = input("Do you want to add more items? (Y/N): ").lower()
                if add_more != 'y':
                    # Confirm order and save transaction
                    confirmation = input("Confirm your order? (Y/N): ").lower()
                    if confirmation == 'y':
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        for order in order_list:
                            order['timestamp'] = timestamp
                        self.transactions.extend(order_list)
                        self.save_data(self.transactions, self.transactions_file)
                        print("Order confirmed. Thank you!")
                        break
                    else:
                        print("Order canceled.")
                        break
            else:
                print("Invalid item ID. Please try again.")
                
    def review_item(self):
        self.show_menu()
        item_id = int(input("Enter the item ID you want to review: "))
        item = next((x for x in self.menu if x['id'] == item_id), None)
        if item:
            rating = int(input("Enter your rating (1-5): "))
            item['reviews'].append(rating)
            print("Review added successfully!")
            self.save_data(self.menu, self.menu_file)
        else:
            print("Invalid item ID. Please try again.")

    # FOR ADMINS
    
    def update_menu(self):
        # Load admin data from admins.json
        admin_data = self.load_data(self.admins_file)

        # Take admin credentials input
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        # Check if entered credentials match admin data
        if {"username": username, "password": password} in admin_data:
            self.show_menu()
            item_id = int(input("Enter the item ID you want to update: "))
            item = next((x for x in self.menu if x['id'] == item_id), None)
            if item:
                new_price = float(input("Enter the new price: $"))
                item['price'] = new_price
                print("Menu updated successfully!")
                self.save_data(self.menu, self.menu_file)
            else:
                print("Invalid item ID. Please try again.")
        else:
            print("Authentication failed. You are not an admin.")

    def add_new_product(self):
        # Load admin data from admins.json
        admin_data = self.load_data(self.admins_file)

        # Take admin credentials input
        username = input("\nEnter admin username: ")
        password = input("Enter admin password: ")

        # Check if entered credentials match admin data
        if {"username": username, "password": password} in admin_data:
            # Take input for the new product
            new_id = len(self.menu) + 1
            new_name = input("\nEnter the name of the new product: ")
            new_price = float(input("Enter the price of the new product: $"))
            is_veg = input("Is the new product vegetarian? (Y/N): ").lower() == 'y'

            # Create a new product dictionary
            new_product = {
                "id": new_id,
                "name": new_name,
                "price": new_price,
                "veg": is_veg,
                "reviews": []  # Initially, the new product has no reviews
            }

            # Add the new product to the menu
            self.menu.append(new_product)

            print(f"New product '{new_name}' added to the menu successfully!")
            self.save_data(self.menu, self.menu_file)
        else:
            print("Authentication failed. You are not an admin.")
            
    def show_transactions(self):
        # Display a table of transactions
        print("\n{:<5} {:<25} {:<10} {:<20} {:<20}".format("S No.", "Name", "Quantity", "Total Price ($)", "Date Time"))
        print("=" * 90)

        total_price = 0
        for idx, transaction in enumerate(self.transactions, start=1):
            item = next((x for x in self.menu if x['id'] == transaction['item_id']), None)
            if item:
                total_price += transaction['total_price']
                # Check if 'timestamp' key is present in the transaction
                formatted_datetime = transaction.get('timestamp', 'N/A')
                if formatted_datetime != 'N/A':
                    formatted_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                print("{:<5} {:<25} {:<10} {:<20.2f} {:<20}".format(idx, item['name'], transaction['quantity'], transaction['total_price'], formatted_datetime))

        print("=" * 90)
        print("{:<60} {:<20.2f}".format("Total Price:", total_price))
        print("=" * 90)

    def exit_program(self):
        print("Exiting the Restaurant Management System. Thank you!")

    def run(self):
        while True:
            # Display main menu options
            print("\n------ Restaurant Management System ------")
            print("1. Show Menu")
            print("2. Order Items")
            print("3. Show Order History")
            print("4. Update Menu (Admin Only)")
            print("5. Add New Item to Menu (Admin Only)")
            print("6. Review Item")
            print("7. Exit")

            # Take user input for menu choice
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                self.show_menu()
            elif choice == '2':
                self.order_items()
            elif choice == '3':
                self.show_transactions()
            elif choice == '4':
                self.update_menu()
            elif choice == '5':
                self.add_new_product()
            elif choice == '6':
                self.review_item()
            elif choice == '7':
                self.exit_program()
                break
            else:
                print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    # Initialize and run the RestaurantManager
    restaurant_manager = RestaurantManager()
    restaurant_manager.run()
