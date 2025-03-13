import sqlite3

from config import DB_NAME


def list_of_interns(admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    interns_username = cursor.execute(f'''SELECT username FROM Interns WHERE admin={admin}''').fetchall()
    interns_username = [i[0] for i in interns_username]
    interns_snm = interns_username
    # interns_snm = cursor.execute(f'''SELECT surname, name, middle_name FROM Interns WHERE username in {interns_username}''') ???
    return interns_snm

