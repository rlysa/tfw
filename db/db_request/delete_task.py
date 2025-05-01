import sqlite3

from config import DB_NAME


def delete_task(tasks_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM Tasks WHERE id="{tasks_id}"')
    connection.commit()
    connection.close()
