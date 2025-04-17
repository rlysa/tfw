import sqlite3
from typing import Optional
from config import DB_NAME
import logging

logger = logging.getLogger(__name__)


def get_group_composition(user_username: str) -> Optional[dict]:
    """Находит группу пользователя и возвращает её состав"""
    try:
        if not user_username:
            return None

        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Ищем группу, где пользователь является админом
            cursor.execute("""
                SELECT id, name, admin, interns 
                FROM Groups
                WHERE admin = ?
            """, (user_username.lower(),))
            group_as_admin = cursor.fetchone()

            # Ищем группу, где пользователь является стажёром
            cursor.execute("""
                SELECT id, name, admin, interns 
                FROM Groups
                WHERE interns LIKE ? OR interns LIKE ? OR interns = ?
            """, (
                f"{user_username.lower()} %",
                f"% {user_username.lower()}",
                user_username.lower()
            ))
            group_as_intern = cursor.fetchone()

            # Объединяем результаты (пользователь может быть только в одной группе)
            group = group_as_admin or group_as_intern

            if not group:
                return None

            # Получаем информацию об админе группы
            cursor.execute("""
                SELECT surname, name, middle_name 
                FROM Users 
                WHERE username = ?
            """, (group['admin'],))
            admin = cursor.fetchone()

            if not admin:
                return None

            admin_info = {
                'full_name': f"{admin['surname']} {admin['name']} {admin['middle_name']}",
                'username': group['admin']
            }

            # Обрабатываем стажёров
            interns_info = []
            interns = group['interns'] or ""

            # Разделяем строку стажёров и фильтруем пустые значения
            intern_usernames = [u.strip() for u in interns.split() if u.strip()]

            for intern_username in intern_usernames:
                if intern_username.lower() == user_username.lower():
                    continue  # Пропускаем текущего пользователя

                cursor.execute("""
                    SELECT surname, name, middle_name 
                    FROM Users 
                    WHERE username = ?
                """, (intern_username,))
                intern = cursor.fetchone()

                if intern:
                    interns_info.append({
                        'full_name': f"{intern['surname']} {intern['name']} {intern['middle_name']}",
                        'username': intern_username
                    })

            return {
                'group_name': group['name'],
                'admin_info': admin_info,
                'interns_info': interns_info,
                'current_user_in_group': True
            }

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None