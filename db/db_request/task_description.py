import sqlite3
from typing import Optional, Tuple
from config import DB_NAME
import logging

logger = logging.getLogger(__name__)


def get_task_description(task_id: int) -> Optional[Tuple[str, str, str, str]]:
    """
    Получает полное описание задачи по её ID

    Args:
        task_id: ID задачи

    Returns:
        Кортеж (name, description, deadline, status) или None если задача не найдена
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, description, deadline, done 
                FROM Tasks 
                WHERE id = ?
            """, (task_id,))

            task = cursor.fetchone()
            if task:
                name, description, deadline, done = task
                status = "✅ Завершена" if done else "🔄 В работе"
                return name, description, deadline, status
            return None

    except sqlite3.Error as e:
        logger.error(f"Database error in get_task_description: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in get_task_description: {e}")
        return None


def change_task_status(task_id: int) -> bool:
    """
    Изменяет статус задачи на противоположный

    Args:
        task_id: ID задачи

    Returns:
        True если статус изменен успешно, False при ошибке
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Получаем текущий статус
            cursor.execute("SELECT done FROM Tasks WHERE id = ?", (task_id,))
            current_status = cursor.fetchone()[0]

            # Инвертируем статус
            new_status = not current_status
            cursor.execute(
                "UPDATE Tasks SET done = ? WHERE id = ?",
                (new_status, task_id)
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        logger.error(f"Database error in change_task_status: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in change_task_status: {e}")
        return False