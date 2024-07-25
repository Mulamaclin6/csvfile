import csv
import os

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price}, {self.quantity}"

class ProductManager:
    def __init__(self, filename):
        self.filename = filename
        self.products = []
        self.load_products()

    def load_products(self):
        """Loads products from the CSV file, handling missing files and invalid data rows."""
        if not os.path.exists(self.filename):
            print(f"{self.filename} not found. Starting with an empty product list.")
            return
        
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip the header row if it exists
                for row in reader:
                    if len(row) != 3:
                        print(f"Skipping invalid row: {row}")
                        continue
                    name, price, quantity = row
                    try:
                        self.products.append(Product(name, float(price), int(quantity)))
                    except ValueError:
                        print(f"Skipping invalid row with non-numeric values: {row}")
        except Exception as e:
            print(f"Error reading {self.filename}: {e}")

    def save_products(self):
        """Saves the product list to the CSV file."""
        try:
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Price", "Quantity"])  # Write header row
                for product in self.products:
                    writer.writerow([product.name, product.price, product.quantity])
        except Exception as e:
            print(f"Error writing to {self.filename}: {e}")

    def add_product(self, name, price, quantity):
        """Adds a new product to the list and saves the updated list to the CSV file."""
        self.products.append(Product(name, price, quantity))
        self.save_products()

    def view_products(self):
        """Displays all products in the list."""
        if not self.products:
            print("No products available.")
            return
        for product in self.products:
            print(product)

    def update_product(self, name, new_name, new_price, new_quantity):
        """Updates an existing product's details and saves the updated list to the CSV file."""
        for product in self.products:
            if product.name == name:
                product.name = new_name
                product.price = new_price
                product.quantity = new_quantity
                self.save_products()
                return
        print(f"Product with name '{name}' not found.")

    def delete_product(self, name):
        """Deletes a product from the list and saves the updated list to the CSV file."""
        self.products = [product for product in self.products if product.name != name]
        self.save_products()

def get_valid_input(prompt, type_):
    """Gets valid input of the specified type from the user, handling invalid inputs."""
    while True:
        try:
            return type_(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {type_.__name__}.")

def main():
    filename = 'products.csv'
    manager = ProductManager(filename)

    while True:
        print("\nProduct Management System")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = get_valid_input("Enter product price: ", float)
            quantity = get_valid_input("Enter product quantity: ", int)
            manager.add_product(name, price, quantity)
        elif choice == '2':
            manager.view_products()
        elif choice == '3':
            name = input("Enter product name to update: ")
            new_name = input("Enter new product name: ")
            new_price = get_valid_input("Enter new product price: ", float)
            new_quantity = get_valid_input("Enter new product quantity: ", int)
            manager.update_product(name, new_name, new_price, new_quantity)
        elif choice == '4':
            name = input("Enter product name to delete: ")
            manager.delete_product(name)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
