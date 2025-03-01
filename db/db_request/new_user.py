import sqlite3

from config import DB_NAME


def new_user(username, role, name, surname, middle_name):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Users (username, role, name, surname, middle_name)
VALUES (?, ?, ?, ?, ?)''',
                   (username, role, name, surname, middle_name))
    connection.commit()
    connection.close()
