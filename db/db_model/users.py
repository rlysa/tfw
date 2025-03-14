import sqlite3

from config import DB_NAME


def users():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
username TEXT PRIMARY KEY,
role INTEGER,
surname TEXT,
name TEXT,
middle_name TEXT
)
''')
    connection.commit()
    connection.close()
