import sqlite3

from config import DB_NAME


def profile(username):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    key = cursor.execute(f'SELECT key FROM Admins WHERE username="{username}"').fetchone()[0]
    fio = cursor.execute(f'SELECT surname, name, middle_name FROM Users WHERE username="{username}"').fetchone()
    return key, ' '.join([i for i in fio])
