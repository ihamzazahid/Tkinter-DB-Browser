import tkinter as tk
from tkinter import messagebox

def add_column(conn, table):
    win = tk.Toplevel()
    win.title("Add Column")

    tk.Label(win, text="Column Name").grid(row=0, column=0)
    tk.Label(win, text="Type (e.g. VARCHAR(255))").grid(row=1, column=0)

    name = tk.Entry(win)
    dtype = tk.Entry(win)

    name.grid(row=0, column=1)
    dtype.grid(row=1, column=1)

    def save():
        cursor = conn.cursor()
        try:
            cursor.execute(f"ALTER TABLE {table} ADD {name.get()} {dtype.get()}")
            conn.commit()
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Add", command=save).grid(row=2, column=1)

def remove_column(conn, table, column):
    cursor = conn.cursor()
    cursor.execute(f"ALTER TABLE {table} DROP COLUMN {column}")
    conn.commit()
