import sqlite3

from config import DB_NAME


def delete_group(groups_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM Groups WHERE id="{groups_id}"')
    connection.commit()
    connection.close()
