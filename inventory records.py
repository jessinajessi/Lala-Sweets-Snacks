import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Database Setup ---
conn = sqlite3.connect("lala_users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        item TEXT,
        quantity INTEGER,
        price REAL
    )
""")
conn.commit()

# --- Main Window ---
root = tk.Tk()
root.geometry('900x600')
root.title("Lala Sweet & Snacks - Inventory Records")
root.configure(bg="#F0A664")

label = tk.Label(root, text="Lala Sweet & Snacks", font=("Arial", 16, "bold"),
                 fg="red", bg="#64ABE6")
label.pack(pady=20)

# --- Form Section ---
form_frame = tk.Frame(root, bg="#8cff1a", padx=10, pady=10)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Item Name:", bg="#e60099", fg="white").grid(row=0, column=0, padx=5, pady=5)
item_entry = tk.Entry(form_frame, width=15)
item_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Quantity:", bg="#e60099", fg="white").grid(row=1, column=0, padx=5, pady=5)
qty_entry = tk.Entry(form_frame, width=15)
qty_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Price:", bg="#e60099", fg="white").grid(row=2, column=0, padx=5, pady=5)
price_entry = tk.Entry(form_frame, width=15)
price_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(form_frame, text="Add Item", command=lambda: add_item(), bg="#ff086b", fg="white")\
    .grid(row=3, column=0, columnspan=2, pady=5)

tk.Button(form_frame, text="Delete Item", command=lambda: delete_item(), bg="#ff086b", fg="white")\
    .grid(row=4, column=0, columnspan=2, pady=5)

tk.Button(form_frame, text="Show Inventory", command=lambda: show_inventory(), bg="#ff086b", fg="white")\
    .grid(row=5, column=0, columnspan=2, pady=5)

# --- Treeview ---
tree = ttk.Treeview(root, columns=("Name", "Quantity", "Price"), show="headings")
tree.heading("Name", text="Item Name")
tree.heading("Quantity", text="Quantity")
tree.heading("Price", text="Price")
tree.pack(pady=10)

# --- Output Text ---
output_text = tk.Text(root, height=5, width=70, bg="white", font=("Courier", 10))
output_text.pack(pady=10)

# --- Functions ---

def load_data():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM inventory")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def add_item():
    item = item_entry.get().strip()
    qty = qty_entry.get().strip()
    price = price_entry.get().strip()

    if not item or not qty.isdigit() or not price.replace(".", "", 1).isdigit():
        messagebox.showwarning("Invalid Input", "Please enter valid item, quantity (int), and price (float).")
        return

    cursor.execute("INSERT INTO inventory VALUES (?, ?, ?)", (item, int(qty), float(price)))
    conn.commit()
    load_data()
    clear_entries()

def delete_item():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an item to delete.")
        return

    for item_id in selected_item:
        item_values = tree.item(item_id)["values"]
        cursor.execute("DELETE FROM inventory WHERE item=? AND quantity=? AND price=?",
                       (item_values[0], int(item_values[1]), float(item_values[2])))
        conn.commit()
        tree.delete(item_id)

def show_inventory():
    output_text.delete(1.0, tk.END)
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()

    if not rows:
        output_text.insert(tk.END, "Inventory is empty.\n")
        return

    total_qty = 0
    total_value = 0.0

    output_text.insert(tk.END, f"{'Item':<25}{'Qty':<10}{'Price':<10}\n")
    output_text.insert(tk.END, "-" * 50 + "\n")

    for item, qty, price in rows:
        output_text.insert(tk.END, f"{item:<25}{qty:<10}{price:<10.2f}\n")
        total_qty += qty
        total_value += qty * price

    output_text.insert(tk.END, "-" * 50 + "\n")
    output_text.insert(tk.END, f"{'TOTAL':<25}{total_qty:<10}{total_value:<10.2f}\n")

def clear_entries():
    item_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

load_data()

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
