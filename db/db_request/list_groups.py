import sqlite3

from config import DB_NAME


def list_of_groups(admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    groups_name = cursor.execute(f'''SELECT id, name FROM Groups WHERE admin="{admin}"''').fetchall()
    return groups_name
