from db.mysql_db import mysql_connect
from db.postgres_db import postgres_connect
from db.mssql_db import mssql_connect


def connect(*, db_type, host, port, user, password):
    """
    Keyword-only arguments prevent positional bugs
    """
    if db_type == "MySQL":
        return mysql_connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

    elif db_type == "PostgreSQL":
        return postgres_connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

    elif db_type == "MSSQL":
        return mssql_connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

    else:
        raise ValueError("Unsupported database type")
