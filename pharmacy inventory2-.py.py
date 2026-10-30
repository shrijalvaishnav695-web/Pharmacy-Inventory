import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "medicines.csv")
LOW_STOCK_LIMIT = 10


def load_medicines():
    """Load medicine records from the CSV file into a list of dictionaries."""
    medicines = []
    if not os.path.exists(FILE_NAME):
        return medicines

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                medicines.append({
                    "id": row["ID"],
                    "name": row["Name"],
                    "quantity": int(row["Quantity"]),
                    "price": float(row["Price"])
                })
            except (KeyError, ValueError):
                # Skip malformed rows instead of crashing.
                continue
    return medicines


def save_medicines(medicines):
    """Save all medicine records back to the CSV file."""
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        fields = ["ID", "Name", "Quantity", "Price"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for medicine in medicines:
            writer.writerow({
                "ID": medicine["id"],
                "Name": medicine["name"],
                "Quantity": medicine["quantity"],
                "Price": f'{medicine["price"]:.2f}'
            })


def next_medicine_id(medicines):
    """Create the next ID in sequence: M1, M2, M3, ..."""
    highest = 0
    for medicine in medicines:
        medicine_id = medicine["id"]
        if medicine_id.startswith("M") and medicine_id[1:].isdigit():
            highest = max(highest, int(medicine_id[1:]))
    return f"M{highest + 1}"


def find_medicine(medicines, medicine_id):
    for medicine in medicines:
        if medicine["id"].lower() == medicine_id.strip().lower():
            return medicine
    return None


def add_medicine(medicines):
    name = input("Medicine name: ").strip()
    if not name:
        print("Medicine name cannot be empty.")
        return

    try:
        quantity = int(input("Quantity: "))
        price = float(input("Price per unit: "))
    except ValueError:
        print("Invalid input. Quantity must be a whole number and price must be numeric.")
        return

    if quantity < 0 or price < 0:
        print("Quantity and price cannot be negative.")
        return

    medicine = {
        "id": next_medicine_id(medicines),
        "name": name,
        "quantity": quantity,
        "price": price
    }
    medicines.append(medicine)
    save_medicines(medicines)
    print(f'Medicine added. ID: {medicine["id"]} | {medicine["name"]} | '
          f'Qty: {medicine["quantity"]} | Price: {medicine["price"]:.2f}')


def view_medicines(medicines):
    if not medicines:
        print("No medicines found.")
        return

    print("\nID   | Medicine             | Quantity | Price")
    print("-" * 53)
    for medicine in medicines:
        status = " LOW STOCK" if medicine["quantity"] < LOW_STOCK_LIMIT else ""
        print(f'{medicine["id"]:<4} | {medicine["name"]:<20} | '
              f'{medicine["quantity"]:>8} | {medicine["price"]:>8.2f}{status}')


def sell_medicine(medicines):
    medicine_id = input("Medicine ID: ").strip()
    medicine = find_medicine(medicines, medicine_id)
    if medicine is None:
        print("Medicine ID not found.")
        return

    try:
        quantity = int(input("Quantity to sell: "))
    except ValueError:
        print("Invalid quantity. Enter a whole number.")
        return

    if quantity <= 0:
        print("Sale quantity must be greater than zero.")
        return

    if quantity > medicine["quantity"]:
        print(f'Insufficient stock. Available: {medicine["quantity"]}')
        return

    bill = quantity * medicine["price"]
    medicine["quantity"] -= quantity
    save_medicines(medicines)
    print(f"Sold {quantity} unit(s). Bill: {bill:.2f}")
    if medicine["quantity"] < LOW_STOCK_LIMIT:
        print(f'Low stock alert: only {medicine["quantity"]} unit(s) left.')


def delete_medicine(medicines):
    medicine_id = input("Medicine ID to delete: ").strip()
    medicine = find_medicine(medicines, medicine_id)
    if medicine is None:
        print("Medicine ID not found.")
        return

    medicines.remove(medicine)
    save_medicines(medicines)
    print(f'Medicine {medicine_id.upper()} deleted.')


def low_stock_report(medicines):
    low_stock = [m for m in medicines if m["quantity"] < LOW_STOCK_LIMIT]
    if not low_stock:
        print("No medicines are currently low on stock.")
        return

    print("\nLOW STOCK REPORT (quantity below 10)")
    for medicine in low_stock:
        print(f'{medicine["id"]} | {medicine["name"]} | Qty: {medicine["quantity"]}')


def inventory_value(medicines):
    total = sum(medicine["quantity"] * medicine["price"] for medicine in medicines)
    print(f"Total inventory value: {total:.2f}")


def show_menu():
    print("\n========== PHARMACY INVENTORY SYSTEM ==========")
    print("1. Add medicine")
    print("2. View all medicines")
    print("3. Sell medicine")
    print("4. Delete medicine")
    print("5. Low-stock report")
    print("6. Total inventory value")
    print("0. Exit")


def main():
    medicines = load_medicines()
    print("Welcome to the Pharmacy Inventory System!")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_medicine(medicines)
        elif choice == "2":
            view_medicines(medicines)
        elif choice == "3":
            sell_medicine(medicines)
        elif choice == "4":
            delete_medicine(medicines)
        elif choice == "5":
            low_stock_report(medicines)
        elif choice == "6":
            inventory_value(medicines)
        elif choice == "0":
            print("Thank you for using the Pharmacy Inventory System.")
            break
        else:
            print("Invalid menu option. Please choose 0 to 6.")


if __name__ == "__main__":
    main()
