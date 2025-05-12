import sqlite3

from config import DB_NAME


def list_of_interns(admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    if admin == 'all':
        interns_username = cursor.execute(f'''SELECT username FROM Interns''').fetchall()
    else:
        interns_username = cursor.execute(f'''SELECT username FROM Interns WHERE admin="{admin}"''').fetchall()
    interns_username_str = '( "' +  '", "'.join([i[0] for i in interns_username]) + '" )'
    interns_snm = cursor.execute(f'''SELECT surname, name, middle_name, username FROM Users WHERE username in {interns_username_str}''').fetchall()
    interns = [[' '.join(interns_snm[i][:-1]), interns_snm[i][-1]]  for i in range(len(interns_snm))]
    connection.close()
    return interns


def interns_info(username):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    intern = cursor.execute(f'''SELECT surname, name, middle_name FROM Users WHERE username="{username}"''').fetchone()
    interns_skills = cursor.execute(f'''SELECT skills FROM Interns WHERE username="{username}"''').fetchone()
    interns_groups = cursor.execute(f'SELECT name, interns FROM Groups').fetchall()
    interns_groups = [i[0] for i in interns_groups if username in i[1].split()]
    interns_tasks = cursor.execute(f'SELECT name, interns, done FROM Tasks').fetchall()
    interns_tasks = [(f'\U00002705 {i[0]}' if i[2] else i[0]) for i in interns_tasks if username in i[1].split()]
    if not interns_groups:
        interns_groups = ['']
    if not interns_tasks:
        interns_tasks = ['']
    intern = [' '.join([i for i in intern]), interns_skills[0], '\n'.join(interns_groups), '\n'.join(interns_tasks)]
    connection.close()
    return intern


def interns_ids(interns_username):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    interns_username_str = '( "' + '", "'.join(interns_username) + '" )'
    ids = cursor.execute(f'SELECT id FROM Users WHERE username in {interns_username_str}').fetchall()
    connection.close()
    return [i[0] for i in ids]
