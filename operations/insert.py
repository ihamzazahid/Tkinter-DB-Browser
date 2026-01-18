import tkinter as tk

def insert_row(conn, table, columns):
    win = tk.Toplevel()
    win.title("Insert Row")

    entries = {}

    for i, col in enumerate(columns):
        tk.Label(win, text=col).grid(row=i, column=0)
        e = tk.Entry(win)
        e.grid(row=i, column=1)
        entries[col] = e

    def save():
        cursor = conn.cursor()
        values = [entries[c].get() for c in columns]
        query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['%s']*len(values))})"
        cursor.execute(query, values)
        conn.commit()
        win.destroy()

    tk.Button(win, text="Save", command=save).grid(row=len(columns), column=1)
