import sqlite3
from random import choices

from config import DB_NAME


def is_new_user(username):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    usernames = cursor.execute('''SELECT username FROM Users''').fetchall()
    return (username, ) not in usernames


def new_user(username, role, name, surname, middle_name, skills, admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Users (username, role, name, surname, middle_name)
VALUES (?, ?, ?, ?, ?)''',
                   (username, role, name, surname, middle_name))

    if role == 3:
        cursor.execute('''INSERT INTO Interns (username, skills, admin)
        VALUES (?, ?, ?)''',
                       (username, skills, admin))
    else:
        key = ''.join([chr(i) for i in choices(list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123)), k=8)])
        cursor.execute('''INSERT INTO Admins (username, key)
VALUES (?, ?)''',
                       (username, key))

    connection.commit()
    connection.close()
