import sqlite3
from typing import List, Tuple
from config import DB_NAME
import logging


logger = logging.getLogger(__name__)


def list_tasks(intern_username: str) -> List[Tuple[int, str, str, str, str]]:
    """Получает список задач пользователя из БД"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, description, done, deadline 
                FROM Tasks 
                WHERE interns = ?
                ORDER BY deadline ASC
            """, (intern_username,))

            tasks = []
            for task in cursor.fetchall():
                task_id, name, description, done, deadline = task
                status = "completed" if done else "in_progress"
                tasks.append((task_id, name, description, status, deadline))

            return tasks

    except sqlite3.Error as e:
        logger.error(f"Database error in list_tasks: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in list_tasks: {e}")
        return []


def list_of_tasks(admin):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    tasks_names = cursor.execute(f'''SELECT id, name FROM Tasks WHERE admin="{admin}"''').fetchall()
    connection.close()
    return tasks_names


def tasks_info_admin(id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    tasks = cursor.execute(f'SELECT * FROM Tasks WHERE id="{id}"').fetchall()
    tasks = [i for i in tasks[0]]
    if tasks[-2] == 'no_report':
        tasks[-2] = 'Без отчета'
    elif tasks[-2] == 'message':
        tasks[-2] = 'Сообщение'
    elif tasks[-2] == 'file':
        tasks[-2] = 'Файл'
    connection.close()
    return tasks
