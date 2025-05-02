import sqlite3

from config import DB_NAME


def delete_user(username, role):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM Users WHERE username="{username}"')
    if role == 3:
        cursor.execute(f'DELETE FROM Interns WHERE username="{username}"')
    else:
        cursor.execute(f'DELETE FROM Admins WHERE username="{username}"')
    connection.commit()
    connection.close()
