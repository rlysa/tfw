import sqlite3
from random import choices

import json

from config import DB_NAME


def is_new_user(user_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    ids = cursor.execute('''SELECT id FROM Users''').fetchall()
    if (user_id, ) not in ids:
        connection.close()
        return 'new'
    else:
        role = cursor.execute(f'''SELECT role FROM Users WHERE id="{user_id}"''').fetchone()
        connection.close()
        return role[0]


def new_user(user_id, username, user):
    role, surname, name, middle_name = user['role'], user['surname'], user['name'], user['middle_name']

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Users (id, username, role, surname, name, middle_name) VALUES (?, ?, ?, ?, ?, ?)''',
                   (user_id, username, role, surname, name, middle_name))

    if role == 3:
        admin = cursor.execute(f'''SELECT username FROM Admins WHERE key={user['admin']}''').fetchone()[0]
        cursor.execute('''INSERT INTO Interns (username, skills, admin, resume) VALUES (?, ?, ?, ?)''',
                       (username, user['skills'], admin, json.dumps(user['resume'])))
    else:
        key = int(''.join(choices([f'{i}' for i in range(0, 10)], k=8))) if username != 'admin' else 11111111  # создание админа для тестов, пароль, чтоб не смотреть в бд, потом удалить
        cursor.execute('''INSERT INTO Admins (key, username) VALUES (?, ?)''',
                       (key, username))

    connection.commit()
    connection.close()
