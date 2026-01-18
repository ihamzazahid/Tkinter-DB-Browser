def delete_row(conn, table, tree, pk_col):
    selected = tree.selection()
    if not selected:
        return

    values = tree.item(selected[0])["values"]
    pk_value = values[0]

    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE {pk_col}=%s", (pk_value,))
    conn.commit()
    tree.delete(selected[0])
