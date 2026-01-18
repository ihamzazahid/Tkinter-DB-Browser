import tkinter as tk

def edit_cell(tree, conn, table, pk_col):
    region = tree.identify("region", tree.winfo_pointerx() - tree.winfo_rootx(),
                            tree.winfo_pointery() - tree.winfo_rooty())
    if region != "cell":
        return

    row_id = tree.focus()
    column = tree.identify_column(tree.winfo_pointerx() - tree.winfo_rootx())
    col_index = int(column.replace("#", "")) - 1

    x, y, w, h = tree.bbox(row_id, column)
    value = tree.item(row_id)["values"][col_index]

    entry = tk.Entry(tree)
    entry.place(x=x, y=y, width=w, height=h)
    entry.insert(0, value)
    entry.focus()

    def save(event):
        new_value = entry.get()
        values = list(tree.item(row_id)["values"])
        values[col_index] = new_value
        tree.item(row_id, values=values)

        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE {table} SET {tree['columns'][col_index]}=%s WHERE {pk_col}=%s",
            (new_value, values[0])
        )
        conn.commit()
        entry.destroy()

    entry.bind("<Return>", save)
