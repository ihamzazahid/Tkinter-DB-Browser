import tkinter as tk
from tkinter import ttk
from operations.insert import insert_row
from operations.delete import delete_row
from operations.update import edit_cell
from operations.export_csv import export_csv
from operations.column_ops import add_column, remove_column
from utils.helper import get_primary_key
from ui.table_with_filters import TableWithFilters

PAGE_SIZE = 50

def open_table_view(conn, db, table):
    if not db or not table:
        tk.messagebox.showerror("Error", "Please select a database and table.")
        return

    win = tk.Toplevel()
    win.title(f"{db}.{table}")
    win.geometry("900x500")

    cursor = conn.cursor()
    cursor.execute(f"USE `{db}`")

    # Get primary key for editing/deleting
    pk_col = get_primary_key(cursor, table)

    # Fetch first page of rows
    offset = 0
    cursor.execute(f"SELECT * FROM `{table}` LIMIT {PAGE_SIZE} OFFSET {offset}")
    rows = cursor.fetchall()

    # Get column names
    cursor.execute(f"SHOW COLUMNS FROM `{table}`")
    columns = [c[0] for c in cursor.fetchall()]

    # ---------- TableWithFilters ----------
    table_widget = TableWithFilters(win, columns, rows)

    # Bind double-click for cell editing
    table_widget.tree.bind("<Double-1>", lambda e: edit_cell(
        table_widget.tree, conn, table, pk_col
    ))

    # ---------- Buttons ----------
    btns = tk.Frame(win)
    btns.pack(fill="x")

    tk.Button(btns, text="Insert",
              command=lambda: insert_row(conn, table, columns)).pack(side="left")

    tk.Button(btns, text="Delete",
              command=lambda: delete_row(conn, table, table_widget.tree, pk_col)).pack(side="left")

    tk.Button(btns, text="Add Column",
              command=lambda: add_column(conn, table)).pack(side="left")

    tk.Button(btns, text="Remove Column",
              command=lambda: remove_column(conn, table, table_widget.tree["columns"][0])).pack(side="left")

    tk.Button(btns, text="Export CSV",
              command=lambda: export_csv(columns, rows)).pack(side="left")

    # ---------- Pagination ----------
    def next_page():
        nonlocal offset
        offset += PAGE_SIZE
        cursor.execute(f"SELECT * FROM `{table}` LIMIT {PAGE_SIZE} OFFSET {offset}")
        new_rows = cursor.fetchall()
        if new_rows:
            table_widget.load_data(new_rows)
        else:
            offset -= PAGE_SIZE  # stay on last page if no rows

    def prev_page():
        nonlocal offset
        offset = max(0, offset - PAGE_SIZE)
        cursor.execute(f"SELECT * FROM `{table}` LIMIT {PAGE_SIZE} OFFSET {offset}")
        table_widget.load_data(cursor.fetchall())

    tk.Button(btns, text="<< Prev", command=prev_page).pack(side="right")
    tk.Button(btns, text="Next >>", command=next_page).pack(side="right")
