import mysql.connector
def db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Hassan@Sanjk7",
        database = "bus_system_db"
    )