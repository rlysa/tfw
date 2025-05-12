import sqlite3

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
