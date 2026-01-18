import mysql.connector

def mysql_connect(host, port, user, password):
    return mysql.connector.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        auth_plugin="mysql_native_password"  # <--- FORCE this
    )
