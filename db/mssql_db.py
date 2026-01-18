import pyodbc


def mssql_connect(*, host, port, user, password, database="master"):
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={host},{port};"
        f"UID={user};PWD={password};"
        f"DATABASE={database}"
    )
    return pyodbc.connect(conn_str)
