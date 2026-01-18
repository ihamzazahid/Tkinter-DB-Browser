def get_primary_key(cursor, table):
    cursor.execute(f"SHOW KEYS FROM {table} WHERE Key_name='PRIMARY'")
    result = cursor.fetchone()
    return result[4] if result else None
