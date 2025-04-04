import sqlite3
from typing import Optional, Dict
from config import DB_NAME
import logging

logger = logging.getLogger(__name__)


def get_full_user_info(username: str) -> Optional[Dict]:
    """Получает полную информацию о пользователе, включая навыки из Interns"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Получаем основную информацию из Users
            cursor.execute("SELECT * FROM Users WHERE username = ?", (username.lower(),))
            user_data = cursor.fetchone()

            if not user_data:
                return None

            # Получаем навыки из таблицы Interns
            cursor.execute("SELECT skills FROM Interns WHERE username = ?", (username.lower(),))
            intern_data = cursor.fetchone()

            result = dict(user_data)
            if intern_data and intern_data['skills']:
                result['intern_skills'] = intern_data['skills']

            return result

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None