import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

conn = sqlite3.connect("lala_users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        quantity INTEGER,
        unit_price REAL,
        total REAL,
        timestamp TEXT
    )
""")
conn.commit()

root = tk.Tk()
root.geometry('900x600')
root.title("Lala Sweets & Snacks - Sales Report")
root.configure(bg="#F0A664")

label = tk.Label(root, text="Lala Sweet & Snacks", font=("Arial", 16, "bold"),
                 fg="red", bg="#64ABE6")
label.pack(pady=20)

form_frame = tk.Frame(root, bg="#e6ffff", padx=10, pady=10)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Item Name:", bg="#4dd0e1").grid(row=0, column=0, sticky="e")
item_entry = tk.Entry(form_frame)
item_entry.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Quantity:", bg="#4dd0e1").grid(row=1, column=0, sticky="e")
quantity_entry = tk.Entry(form_frame)
quantity_entry.grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Unit Price:", bg="#4dd0e1").grid(row=2, column=0, sticky="e")
price_entry = tk.Entry(form_frame)
price_entry.grid(row=2, column=1, padx=5)

sales_data = []

def add_sale():
    item = item_entry.get().strip()
    qty = quantity_entry.get().strip()
    price = price_entry.get().strip()

    try:
        qty = int(qty)
        price = float(price)
        if not item or qty <= 0 or price < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid item, positive quantity, and non-negative price.")
        return

    total = qty * price
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO sales (item, quantity, unit_price, total, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (item, qty, price, total, timestamp))
    conn.commit()

    sales_data.append({"item": item, "qty": qty, "price": price, "total": total})
    update_table()

    item_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)


def update_table():
    for row in tree.get_children():
        tree.delete(row)
    total_sum = 0
    for sale in sales_data:
        tree.insert("", "end", values=(sale["item"], sale["qty"], sale["price"], sale["total"]))
        total_sum += sale["total"]
    total_label.config(text=f"Grand Total: ₹{total_sum:.2f}")

def save_report():
    cursor.execute("SELECT item, quantity, unit_price, total FROM sales")
    sales_data = cursor.fetchall()

    if not sales_data:
        messagebox.showinfo("Info", "No sales to save.")
        return

    filename = f"SweetBrew_DailySales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Sweet Brew Cafe - Daily Sales Report\n")
            f.write("Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            f.write(f"{'Item':<20}{'Qty':<10}{'Unit Price':<15}{'Total'}\n")
            f.write("-" * 55 + "\n")

            grand_total = 0
            for item, qty, price, total in sales_data:
                f.write(f"{item:<20}{qty:<10}{price:<15.2f}{total:.2f}\n")
                grand_total += total

            f.write("-" * 55 + "\n")
            f.write(f"{'':<45}Grand Total: ₹{grand_total:.2f}\n")

        messagebox.showinfo("Success", f"Report saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save report:\n{str(e)}")




tk.Button(form_frame, text="Add Sale", bg="#272b91", fg="white", command=add_sale).grid(row=3, column=0, columnspan=2, pady=10)

tree = ttk.Treeview(root, columns=("Item", "Qty", "Price", "Total"), show="headings")
tree.heading("Item", text="Item")
tree.heading("Qty", text="Quantity")
tree.heading("Price", text="Unit Price")
tree.heading("Total", text="Total")
tree.column("Item", anchor="center")
tree.column("Qty", anchor="center")
tree.column("Price", anchor="center")
tree.column("Total", anchor="center")
tree.pack(padx=20, pady=10, fill="x")

total_label = tk.Label(root, text="Grand Total: ₹0.00", font=("Arial", 14), bg="#e0613a")
total_label.pack(pady=5)

tk.Button(root, text="Save Report", bg="#d9048b", fg="white", command=save_report).pack()

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()