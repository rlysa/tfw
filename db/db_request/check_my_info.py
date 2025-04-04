import sqlite3
from typing import Optional
from config import DB_NAME
import logging

logger = logging.getLogger(__name__)

def get_user_info(username: str) -> Optional[dict]:
    """Получает информацию о пользователе по его username"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT surname, name, middle_name, role 
                FROM Users 
                WHERE username = ?
            """, (username.lower(),))

            user = cursor.fetchone()

            if not user:
                return None

            return {
                'surname': user['surname'],
                'name': user['name'],
                'middle_name': user['middle_name'],
                'role': user['role'],
                'username': username
            }

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None