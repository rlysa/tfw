import sqlite3
import re

from config import DB_NAME


def enhance_search_with_regex(word, skill_query) -> list:
    try:
        pattern = re.compile(rf"\b{re.escape(word)}\b", flags=re.IGNORECASE)
        skill_query = skill_query.split()
        return [item for item in skill_query if pattern.search(item)]
    except Exception as e:
        return []


def skill_search_interns(word, admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    interns_skills = cursor.execute(f'SELECT username, skills FROM Interns WHERE admin="{admin}"').fetchall()
    result = []
    for i in interns_skills:
        if enhance_search_with_regex(word, i[1]):
            intern = cursor.execute(f'SELECT surname, name, middle_name FROM Users WHERE username="{i[0]}"').fetchone()
            result.append(f'{" ".join(intern)} - @{i[0]}\n{i[1]}')
    connection.close()
    return result
