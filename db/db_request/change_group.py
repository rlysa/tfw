import sqlite3

from config import DB_NAME


def change_groups_info(groups_id, field, value):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute('UPDATE Groups SET {0}="{1}" WHERE id="{2}"'.format(field, value, groups_id))
        connection.commit()
        connection.close()
        return True
    except Exception:
        return False
