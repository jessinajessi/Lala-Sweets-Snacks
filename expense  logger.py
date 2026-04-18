import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import csv

conn = sqlite3.connect("lala_users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    )
""")
conn.commit()

root = tk.Tk()
root.geometry('900x600')
root.title("Lala Sweet & Snacks - Expense Logger")
root.configure(bg="#F0A664")

label = tk.Label(root, text="Lala Sweet & Snacks", font=("Arial", 16, "bold"),
                 fg="red", bg="#64ABE6")
label.pack(pady=20)

entry_frame = tk.Frame(root, bg="#00ffff")
entry_frame.pack(pady=10)

tk.Label(entry_frame, text="Date (YYYY-MM-DD):", bg="#d11576").grid(row=0, column=0, sticky='w')
date_entry = tk.Entry(entry_frame)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
date_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(entry_frame, text="Category:", bg="#d11576").grid(row=1, column=0, sticky='w')
category_entry = tk.Entry(entry_frame)
category_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(entry_frame, text="Amount (₹):", bg="#d11576").grid(row=2, column=0, sticky='w')
amount_entry = tk.Entry(entry_frame)
amount_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(entry_frame, text="Description:", bg="#d11576").grid(row=3, column=0, sticky='w')
desc_entry = tk.Entry(entry_frame, width=40)
desc_entry.grid(row=3, column=1, padx=10, pady=5)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview.Heading",
                background="#d318d6",
                foreground="black",
                font=('Arial', 10, 'bold'))

tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Description"), show="headings")
tree.heading("Date", text="Date")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Description", text="Description")

tree.column("Date", width=40, anchor="center")
tree.column("Category", width=200)
tree.column("Amount", width=150)
tree.column("Description", width=150)
tree.pack(padx=20, pady=10, fill="both", expand=True)

def clear_form():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = desc_entry.get()

    if not date or not category or not amount:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return

    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()
    messagebox.showinfo("Success", "Expense logged successfully.")
    clear_form()
    load_expenses()

def load_expenses():
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT date, category, amount, description FROM expenses ORDER BY id DESC")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def export_to_csv():
    cursor.execute("SELECT date, category, amount, description FROM expenses")
    rows = cursor.fetchall()
    with open("sweet_expenses.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])
        writer.writerows(rows)
    messagebox.showinfo("Exported", "Expenses exported to sweet_expenses.csv")


btn_frame = tk.Frame(root, bg="#00ffff")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Expense", command=add_expense, bg="#ed1a80", fg="white",
          padx=10, pady=5).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Clear", command=clear_form, bg="#fc0f4a", fg="white",
          padx=10, pady=5).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Export to CSV", command=export_to_csv, bg="#1541d1", fg="white",
          padx=10, pady=5).grid(row=0, column=2, padx=10)

load_expenses()

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()
