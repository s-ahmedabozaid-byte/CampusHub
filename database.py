import mysql.connector

def DbConnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="annoucement_notify",
        autocommit=True
    )
