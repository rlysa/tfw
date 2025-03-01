import sqlite3

from config import DB_NAME


def interns():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Interns (
username INTEGER PRIMARY KEY,
skills TEXT,
head TEXT
)
''')
    connection.commit()
    connection.close()
