import tkinter as tk
from tkinter import ttk, messagebox
from ui.table_view import open_table_view

def open_main_window(conn):
    root = tk.Tk()
    root.title("Hamza's Database Browser")
    root.geometry("400x200")

    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    dbs = [d[0] for d in cursor.fetchall()]

    tk.Label(root, text="Select Database:").pack(pady=(10,0))
    db_combo = ttk.Combobox(root, values=dbs, state="readonly")
    db_combo.pack(padx=10, pady=5)

    tk.Label(root, text="Select Table:").pack(pady=(10,0))
    table_combo = ttk.Combobox(root, state="readonly")
    table_combo.pack(padx=10, pady=5)

    def load_tables(event):
        db_name = db_combo.get()
        if not db_name:
            return
        try:
            cursor.execute(f"USE `{db_name}`")
            cursor.execute("SHOW TABLES")
            tables = [t[0] for t in cursor.fetchall()]
            table_combo["values"] = tables
            table_combo.set('')  # Clear previous selection
        except Exception as e:
            messagebox.showerror("Error", str(e))

    db_combo.bind("<<ComboboxSelected>>", load_tables)

    tk.Button(
        root,
        text="Open Table",
        command=lambda: open_table_view(conn, db_combo.get(), table_combo.get())
    ).pack(pady=20)

    root.mainloop()
