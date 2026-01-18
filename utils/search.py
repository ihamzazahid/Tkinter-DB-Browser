def filter_rows(rows, search_text):
    if not search_text:
        return rows

    search_text = search_text.lower()
    return [
        r for r in rows
        if any(search_text in str(cell).lower() for cell in r)
    ]
