import sqlite3

from config import DB_NAME


def list_of_groups(admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    groups_name = cursor.execute(f'''SELECT id, name FROM Groups WHERE admin="{admin}"''').fetchall()
    return groups_name


def groups_info(id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    group = cursor.execute(f'''SELECT name, interns FROM Groups WHERE id="{id}"''').fetchone()
    interns_usernames = '( "' + '", "'.join([i for i in group[1].split()]) + '" )'
    interns_names = cursor.execute(f'''SELECT username, surname, name, middle_name FROM Users WHERE username in {interns_usernames}''').fetchall()
    info = [group[0], [' '.join(interns_names[i][1:]) + ' - @' + interns_names[i][0] for i in range(len(interns_names))]]
    return info
