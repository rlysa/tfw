import sqlite3
from random import choices

from config import DB_NAME


def list_of_admins():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    admins_snm = cursor.execute(f'''SELECT surname, name, middle_name, username FROM Users WHERE role=2''').fetchall()
    admins = [[' '.join(admins_snm[i][:-1]), admins_snm[i][-1]]  for i in range(len(admins_snm))]
    connection.close()
    return admins


def admins_info(username):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    admin = cursor.execute(f'''SELECT surname, name, middle_name FROM Users WHERE username="{username}"''').fetchone()
    key = cursor.execute(f'''SELECT key FROM Admins WHERE username="{username}"''').fetchone()
    admin = [' '.join([i for i in admin]), key[0]]
    connection.close()
    return admin


def new_keys():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    admins = cursor.execute(f'''SELECT username FROM Admins''').fetchall()
    for i in admins:
        key = int(''.join(choices([f'{i}' for i in range(0, 10)],
                                  k=8))) if i[0] != 'admin' else 11111111
        cursor.execute('''UPDATE Admins SET key="{0}" WHERE username="{1}"'''.format(key, i[0]))
    connection.commit()
    connection.close()
