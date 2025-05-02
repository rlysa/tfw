import sqlite3

from config import DB_NAME


def skill_search_interns(word):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    interns_skills = cursor.execute('SELECT username, skills FROM Interns').fetchall()
    return 'user3'
