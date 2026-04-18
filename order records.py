import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

conn = sqlite3.connect('lala_users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_name TEXT,
        item TEXT,
        quantity INTEGER,
        order_type TEXT
    )
''')
conn.commit()

def submit_order():
    order = {
        "Order ID": order_id.get(),
        "Customer Name": customer_name.get(),
        "Item": item_name_entry.get(),
        "Quantity": quantity_spinbox.get(),
        "Order Type": order_type_var.get()
    }

    if not all(order.values()):
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return
    cursor.execute('''
                INSERT INTO orders (order_id, customer_name, item, quantity, order_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (
        order["Order ID"],
        order["Customer Name"],
        order["Item"],
        order["Quantity"],
        order["Order Type"]
    ))
    conn.commit()

    messagebox.showinfo("Order Submitted", f"Order for {order['Customer Name']} submitted successfully!")
    clear_fields()

def view_orders():
    view_window = tk.Toplevel(root)
    view_window.title("All Orders")
    view_window.geometry("600x400")

    tree = ttk.Treeview(view_window, columns=("Order ID", "Customer Name", "Item", "Quantity", "Order Type"),
                        show='headings')
    tree.heading("Order ID", text="Order ID")
    tree.heading("Customer Name", text="Customer Name")
    tree.heading("Item", text="Item")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Order Type", text="Order Type")
    tree.pack(fill=tk.BOTH, expand=True)

    cursor.execute("SELECT * FROM orders")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)


def clear_fields():
    order_id.delete(0, tk.END)
    customer_name.delete(0, tk.END)
    item_name_entry.delete(0, tk.END)
    quantity_spinbox.delete(0, tk.END)
    quantity_spinbox.insert(0, "1")
    order_type_var.set("Dine-in")



root = tk.Tk()
root.geometry('900x600')
root.title("Lala Sweets & Snacks - Order Records")
root.configure(bg="#F0A664")

label = tk.Label(root, text="Lala Sweets & Snacks", font=("Arial", 16, "bold"),
                 fg="red", bg="#64ABE6")
label.pack(pady=20)

form_frame = tk.Frame(root, bg="#D44374")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Order Id:", bg="#cd76e3").grid(row=0, column=0, padx=10, pady=5, sticky="e")
order_id = tk.Entry(form_frame, width=30)
order_id.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Customer Name:", bg="#cd76e3").grid(row=1, column=0, padx=10, pady=5, sticky="e")
customer_name = tk.Entry(form_frame, width=30)
customer_name.grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Item Name:", bg="#cd76e3").grid(row=2, column=0, padx=10, pady=5, sticky="e")
item_name_entry = tk.Entry(form_frame, width=30)
item_name_entry.grid(row=2, column=1)

tk.Label(form_frame, text="Quantity:", bg="#cd76e3").grid(row=3, column=0, padx=10, pady=5, sticky="e")
quantity_spinbox = tk.Spinbox(form_frame, from_=1, to=20, width=28)
quantity_spinbox.grid(row=3, column=1)

tk.Label(form_frame, text="Order Type:", bg="#cd76e3").grid(row=4, column=0, padx=10, pady=5, sticky="e")
order_type_var = tk.StringVar(value="Dine-in")
order_type_menu = ttk.Combobox(form_frame, textvariable=order_type_var, values=["Dine-in", "Takeaway"], state="readonly", width=28)
order_type_menu.grid(row=4, column=1)


button_frame = tk.Frame(root, bg="#D44374")
button_frame.pack(pady=10)

submit_btn = tk.Button(button_frame, text="Submit Order", bg="#a83295", fg="white", width=15, command=submit_order)
submit_btn.grid(row=0, column=0, padx=10)

view_btn = tk.Button(button_frame, text="View Orders", bg="#a83295", fg="white", width=15, command=view_orders)
view_btn.grid(row=0, column=2, padx=10)


clear_btn = tk.Button(button_frame, text="Clear", bg="#a83295", fg="white", width=10, command=clear_fields)
clear_btn.grid(row=0, column=1, padx=10)

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()