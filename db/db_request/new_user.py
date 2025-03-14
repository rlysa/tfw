import sqlite3
from random import choices

from config import DB_NAME


def is_new_user(username):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    usernames = cursor.execute('''SELECT username FROM Users''').fetchall()
    if (username, ) not in usernames:
        connection.close()
        return True
    else:
        role = cursor.execute(f'''SELECT role FROM Users WHERE username="{username}"''').fetchone()
        connection.close()
        return role[0]


def new_user(username, user):
    role, surname, name, middle_name = user['role'], user['surname'], user['name'], user['middle_name']

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Users (username, role, surname, name, middle_name) VALUES (?, ?, ?, ?, ?)''',
                   (username, role, surname, name, middle_name))

    if role == 3:
        admin = cursor.execute(f'''SELECT username FROM Admins WHERE key={user['admin']}''').fetchone()[0]
        cursor.execute('''INSERT INTO Interns (username, skills, admin) VALUES (?, ?, ?)''',
                       (username, user['skills'], admin))
    else:
        key = int(''.join(choices([f'{i}' for i in range(0, 10)], k=8))) if username != 'admin' else 11111111  # создание админа для тестов, пароль, чтоб не смотреть в бд, потом удалить
        cursor.execute('''INSERT INTO Admins (key, username) VALUES (?, ?)''',
                       (key, username))

    connection.commit()
    connection.close()
