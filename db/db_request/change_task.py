import sqlite3

from config import DB_NAME


def change_tasks_info(tasks_id, field, value):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute('UPDATE Tasks SET {0}="{1}" WHERE id="{2}"'.format(field, value, tasks_id))
        connection.commit()
        connection.close()
        return True
    except Exception:
        return False
