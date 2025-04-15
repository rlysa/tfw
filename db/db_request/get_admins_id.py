import sqlite3
from config import DB_NAME


def get_admins_id(key):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    if key.isdigit():
        admins_username = cursor.execute(f'SELECT username FROM Admins WHERE key="{int(key)}"').fetchone()[0]
        admins_id = cursor.execute(f'SELECT id FROM Users WHERE username="{admins_username}"').fetchone()
        return admins_id[0]
    return
