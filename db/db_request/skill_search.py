import sqlite3

from config import DB_NAME


def skill_search_interns(word, admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    interns_skills = cursor.execute(f'SELECT username, skills FROM Interns WHERE admin="{admin}"').fetchall()
    result = []
    for i in interns_skills:
        skills = i[1].split()
        if [j for j in skills if word in j]:
            intern = cursor.execute(f'SELECT surname, name, middle_name FROM Users WHERE username="{i[0]}"').fetchone()
            result.append(f'{" ".join(intern)} - @{i[0]}\n{i[1]}')
    connection.close()
    return result
