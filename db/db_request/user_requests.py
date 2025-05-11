import sqlite3
from config import DB_NAME
import logging
from db.db_model.users import Users

logger = logging.getLogger(__name__)

def get_admin_chat_id(task_admin_username: str) -> int | None:
    """Получает chat_id админа по username из задачи"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id 
                FROM Users 
                WHERE username = ? 
                AND role IN (?, ?)
            """, (task_admin_username, Users.ADMIN_FATHER, Users.ADMIN))
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        logger.error(f"Ошибка получения chat_id админа: {e}")
        return None