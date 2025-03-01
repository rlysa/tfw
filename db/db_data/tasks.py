import sqlite3

from config import DB_NAME


def tasks():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
id INTEGER PRIMARY KEY,
name TEXT,
interns TEXT,
admin TEXT,
description TEXT,
deadline DATE,
report TEXT
)
''')
    connection.commit()
    connection.close()
