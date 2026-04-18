import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

conn = sqlite3.connect("lala_users.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
''')
conn.commit()

root = tk.Tk()
root.geometry('900x600')
root.title("Lala Sweets & Snacks - Menu Items")
root.configure(bg="#F0A664")

label = tk.Label(root, text="Lala Sweets & Snacks", font=("Arial", 16, "bold"),
                 fg="red", bg="#64ABE6")
label.pack(pady=20)

frame = tk.Frame(root, bg="#a83295")
frame.pack(pady=5)

tk.Label(frame, text="Name:", bg="#a83295").grid(row=0, column=0, padx=5, pady=2)
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Category:", bg="#a83295").grid(row=1, column=0, padx=5, pady=2)
category_entry = tk.Entry(frame)
category_entry.grid(row=1, column=1, padx=5)

tk.Label(frame, text="Price ($):", bg="#a83295").grid(row=2, column=0, padx=5, pady=2)
price_entry = tk.Entry(frame)
price_entry.grid(row=2, column=1, padx=5)

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

columns = ("Id", "Name", "Category", "Price")
menu_list = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
for col in columns:
    menu_list.heading(col, text=col)
menu_list.column("Id", width=100)
menu_list.column("Name", width=200)
menu_list.column("Category", width=150)
menu_list.column("Price", width=100)
menu_list.pack()


def refresh_menu():
    for item in menu_list.get_children():
        menu_list.delete(item)

    cursor.execute("SELECT * FROM menu_items")
    for row in cursor.fetchall():
        menu_list.insert("", "end", values=(row[0], row[1], row[2], f'{row[3]:.2f}'))


def clear_fields():
    name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)


def add_item():
    name = name_entry.get()
    category = category_entry.get()
    price = price_entry.get()

    if not name or not category or not price:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        price = float(price)
        cursor.execute("INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)",
                       (name, category, price))
        conn.commit()
        refresh_menu()
        clear_fields()
    except ValueError:
        messagebox.showerror("Input Error", "Price must be a number")


def update_item():
    selected = menu_list.focus()
    if not selected:
        messagebox.showwarning("Select Item", "Select an item to update.")
        return

    item = menu_list.item(selected, 'values')
    if not item:
        return

    try:
        item_id = int(item[0])
        name = name_entry.get()
        category = category_entry.get()
        price = float(price_entry.get())

        cursor.execute("UPDATE menu_items SET name=?, category=?, price=? WHERE id=?",
                       (name, category, price, item_id))
        conn.commit()
        refresh_menu()
        clear_fields()
    except ValueError:
        messagebox.showerror("Update Error", "Invalid input data.")


def delete_item():
    selected = menu_list.focus()
    if not selected:
        messagebox.showwarning("Select Item", "Select an item to delete.")
        return

    item = menu_list.item(selected, 'values')
    if item:
        cursor.execute("DELETE FROM menu_items WHERE id=?", (item[0],))
        conn.commit()
        refresh_menu()
        clear_fields()


def on_item_select(event):
    selected = menu_list.focus()
    if not selected:
        return

    item = menu_list.item(selected, 'values')
    if item:
        name_entry.delete(0, tk.END)
        name_entry.insert(0, item[1])
        category_entry.delete(0, tk.END)
        category_entry.insert(0, item[2])
        price_entry.delete(0, tk.END)
        price_entry.insert(0, item[3])


menu_list.bind("<<TreeviewSelect>>", on_item_select)

btn_frame = tk.Frame(root, bg="#732480")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Add", command=add_item, bg="#db4ba1", fg="white", width=10).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_item, bg="#db4ba1", fg="white", width=10).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_item, bg="#db4ba1", fg="white", width=10).grid(row=0, column=2, padx=5)

refresh_menu()

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
