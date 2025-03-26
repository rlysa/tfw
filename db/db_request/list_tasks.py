import sqlite3
from config import DB_NAME


def list_tasks(intern_username):
    """
    Получает список задач конкретного стажёра
    :param intern_username: username стажера
    :return: список задач в формате [(id, title, description, status, deadline), ...]
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    query = """
    SELECT id, title, description, status, deadline 
    FROM Tasks
    WHERE intern_username=?
    ORDER BY deadline ASC
    """

    tasks = cursor.execute(query, (intern_username,)).fetchall()
    connection.close()
    return tasks