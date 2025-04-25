import sqlite3

from config import DB_NAME


def new_group(name, admin, interns):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Groups (name, admin, interns) VALUES (?, ?, ?)''',
                   (name, admin, interns))
    connection.commit()
    connection.close()
