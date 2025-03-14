import sqlite3

from config import DB_NAME


def admins():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Admins (
key INTEGER PRIMARY KEY,
username TEXT
)
''')
    connection.commit()
    connection.close()
