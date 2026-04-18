import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

conn = sqlite3.connect("lala_users.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bill (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    total REAL NOT NULL
)''')

conn.commit()

root = tk.Tk()
root.geometry('900x600')
root.title("Lala Sweet & Snacks - Billing System")
root.configure(bg="#F0A664")

label = tk.Label(root, text="Lala Sweet & Snacks", font=("Arial", 16, "bold"),
                 fg="red", bg="#64ABE6")
label.pack(pady=20)

form_frame = tk.Frame(root, bg="#99ffff")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Item Name:", bg="#a83295", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
item_entry = tk.Entry(form_frame, width=20)
item_entry.grid(row=0, column=1, sticky="w")

tk.Label(form_frame, text="Quantity:", bg="#a83295", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
quantity_entry = tk.Entry(form_frame, width=20)
quantity_entry.grid(row=1, column=1, sticky="w")

tk.Label(form_frame, text="Price:", bg="#a83295", fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
price_entry = tk.Entry(form_frame, width=20)
price_entry.grid(row=2, column=1, sticky="w")

order_items = []

output_frame = tk.Frame(root, bg="#4fc9c7")
output_frame.pack(pady=10)

bill_text = tk.Text(output_frame, height=10, width=50)
bill_text.grid(row=1, column=0, columnspan=2, pady=10)

total_label = tk.Label(root, text="Total: ₹0.00", font=("Arial", 14, "bold"), bg="#4fc9c7")
total_label.pack()

def add_item():
    item_name = item_entry.get()
    try:
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for quantity and price.")
        return

    cost = quantity * price
    order_items.append({'item': item_name, 'quantity': quantity, 'price': price, 'total': cost})
    bill_text.insert("end", f"{item_name}: {quantity} x {price} = {cost:.2f}\n")

    cursor.execute('''
            INSERT INTO bill (item_name, quantity, price, total)
            VALUES (?, ?, ?, ?)
        ''', (item_name, quantity, price, cost))
    conn.commit()

    item_entry.delete(0, "end")
    quantity_entry.delete(0, "end")
    price_entry.delete(0, "end")


    update_total()

def update_total():
    total = sum(item['total'] for item in order_items)
    total_label.config(text=f"Total: ₹{total:.2f}")

def generate_bill():
    if not order_items:
        messagebox.showwarning("No items", "No items have been added to the bill.")
        return

    bill_text.insert("end", "\n--- Final Bill ---\n")
    total = sum(item['total'] for item in order_items)
    bill_text.insert("end", f"Total Due: ₹{total:.2f}\n")
    bill_text.insert("end", "Thank you for visiting Lala Sweet & Snacks!\n")


output_frame = tk.Frame(root, bg="#4fc9c7")
output_frame.pack(pady=10)

add_button = tk.Button(output_frame, text="Add Item", command=add_item, bg="#a83295")
add_button.grid(row=0, column=0, padx=5)


generate_button = tk.Button(output_frame, text="Generate Bill", command=generate_bill,
                            bg="green", fg="white", font=("Arial", 12))
generate_button.grid(row=0, column=1, padx=5)

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()