import sqlite3

from config import DB_NAME


def list_of_interns(admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    interns_username = cursor.execute(f'''SELECT username FROM Interns WHERE admin="{admin}"''').fetchall()
    interns_username_str = '( "' +  '", "'.join([i[0] for i in interns_username]) + '" )'
    interns_snm = cursor.execute(f'''SELECT surname, name, middle_name FROM Users WHERE username in {interns_username_str}''').fetchall()
    interns = [[' '.join(interns_snm[i]), interns_username[i][0]]  for i in range(len(interns_snm))]
    return interns

