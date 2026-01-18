import psycopg2


def postgres_connect(*, host, port, user, password, database="postgres"):
    return psycopg2.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        dbname=database
    )
