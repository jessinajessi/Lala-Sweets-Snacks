import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

conn = sqlite3.connect("lala_users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        contact TEXT NOT NULL
    )
""")
conn.commit()


root = tk.Tk()
root.geometry('900x600')
root.title("Lala Sweet & Snacks - Staff Records")
root.configure(bg="#F0A664")

label = tk.Label(root, text="Lala Sweet & Snacks", font=("Arial", 16, "bold"),
                 fg="red", bg="#64ABE6")
label.pack(pady=20)

form_frame = tk.LabelFrame(root, text="Add New Staff", bg="#33ffff", padx=10, pady=10)
form_frame.pack(padx=20, pady=20, fill="x")

tk.Label(form_frame, text="Name:", bg="#ff4d4d").grid(row=0, column=0, sticky="e")
name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Role:", bg="#ff4d4d").grid(row=1, column=0, sticky="e")
role_entry = tk.Entry(form_frame, width=30)
role_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Contact:", bg="#ff4d4d").grid(row=2, column=0, sticky="e")
contact_entry = tk.Entry(form_frame, width=30)
contact_entry.grid(row=2, column=1, padx=10, pady=5)

def add_staff():
    name = name_entry.get().strip()
    role = role_entry.get().strip()
    contact = contact_entry.get().strip()

    if not name or not role or not contact:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    cursor.execute("INSERT INTO staff (name, role, contact) VALUES (?, ?, ?)", (name, role, contact))
    conn.commit()
    load_staff()
    messagebox.showinfo("Success", "Staff member added.")

    name_entry.delete(0, tk.END)
    role_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)

def load_staff():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM staff")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to delete.")
        return
    item = tree.item(selected[0])
    staff_id = item['values'][0]

    confirm = messagebox.askyesno("Confirm", "Delete this staff member?")
    if confirm:
        cursor.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
        conn.commit()
        load_staff()
        messagebox.showinfo("Deleted", "Staff record deleted.")

def clear_all():
    confirm = messagebox.askyesno("Confirm", "This will delete ALL staff records. Continue?")
    if confirm:
        cursor.execute("DELETE FROM staff")
        conn.commit()
        load_staff()
        messagebox.showinfo("Cleared", "All staff records have been deleted.")

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview.Heading",
                background="#d318d6",
                foreground="black",
                font=('Arial', 10, 'bold'))

tree = ttk.Treeview(root, columns=("ID", "Name", "Role", "Contact"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Role", text="Role")
tree.heading("Contact", text="Contact")

tree.column("ID", width=40, anchor="center")
tree.column("Name", width=200)
tree.column("Role", width=150)
tree.column("Contact", width=150)

tree.pack(padx=20, pady=10, fill="both", expand=True)

btn_frame = tk.Frame(root, bg="#fff3e0")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Staff", bg="#43a047", fg="white", width=12,
          command=add_staff).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Delete Selected", bg="#e53935", fg="white", width=15,
          command=delete_selected).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Clear All", bg="#f4511e", fg="white", width=12,
          command=clear_all).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Refresh", bg="#039be5", fg="white", width=10,
          command=load_staff).grid(row=0, column=3, padx=10)

load_staff()

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()