import sqlite3

from config import DB_NAME


def groups():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Groups (
id INTEGER PRIMARY KEY,
name TEXT,
admin TEXT,
interns TEXT
)
''')
    connection.commit()
    connection.close()
