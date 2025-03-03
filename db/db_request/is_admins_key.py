import sqlite3

from config import DB_NAME


def is_admins_key(key):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    keys = cursor.execute('''SELECT key FROM Admins''').fetchall()
    connection.close()
    return (key,) in keys
