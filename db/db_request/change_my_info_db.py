import sqlite3
from typing import Optional, Dict
from config import DB_NAME
import logging


logger = logging.getLogger(__name__)


def update_user_info(username: str, update_data: Dict[str, str]) -> bool:
    """Обновляет информацию о пользователе в базе данных"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            # Формируем SQL-запрос на основе переданных данных
            set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
            values = list(update_data.values())
            values.append(username.lower())

            cursor.execute(
                f"UPDATE Users SET {set_clause} WHERE username = ?",
                values
            )

            conn.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as e:
        logger.error(f"Database error when updating user info: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error when updating user info: {e}")
        return False


def update_intern_skills(username: str, new_skills: str) -> bool:
    """Обновляет навыки стажёра в таблице Interns"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE Interns SET skills = ? WHERE username = ?",
                (new_skills, username.lower())
            )

            conn.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as e:
        logger.error(f"Database error when updating intern skills: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error when updating intern skills: {e}")
        return False