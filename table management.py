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
root.title("Lala Sweet & Snacks - Table Management")
root.configure(bg="#F0A664")

label = tk.Label(root, text="Lala Sweet & Snacks", font=("Arial", 16, "bold"),
                 fg="red", bg="#64ABE6")
label.pack(pady=20)

tree = ttk.Treeview(root, columns=("ID", "Item", "Qty", "Price", "Total", "Time"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Item", text="Item")
tree.heading("Qty", text="Quantity")
tree.heading("Price", text="Unit Price")
tree.heading("Total", text="Total")
tree.heading("Time", text="Timestamp")

tree.column("ID", width=40, anchor="center")
tree.column("Item", width=140)
tree.column("Qty", width=80, anchor="center")
tree.column("Price", width=100, anchor="center")
tree.column("Total", width=100, anchor="center")
tree.column("Time", width=200)

tree.pack(pady=20, fill="both", expand=True)

def load_sales():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM sales ORDER BY id DESC")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to delete.")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete the selected sale?")
    if confirm:
        item = tree.item(selected[0])
        sale_id = item['values'][0]
        cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
        conn.commit()
        load_sales()
        messagebox.showinfo("Deleted", "Sale record deleted successfully.")

def clear_all():
    confirm = messagebox.askyesno("Confirm", "This will delete ALL sales records. Are you sure?")
    if confirm:
        cursor.execute("DELETE FROM sales")
        conn.commit()
        load_sales()
        messagebox.showinfo("Cleared", "All sales records have been deleted.")

btn_frame = tk.Frame(root, bg="#80ff80")
btn_frame.pack(pady=10)

(tk.Button(btn_frame, text="Refresh", bg="#cc1f78", fg="white", width=12, command=load_sales)
              .grid(row=0, column=0, padx=10))
(tk.Button(btn_frame, text="Delete Selected", bg="#870f4d", fg="white", width=15, command=delete_selected)
              .grid(row=0, column=1, padx=10))
(tk.Button(btn_frame, text="Clear All Sales", bg="#cc1f78", fg="white", width=15, command=clear_all)
              .grid(row=0, column=2, padx=10))

load_sales()

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
