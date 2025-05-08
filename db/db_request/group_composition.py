import sqlite3
from typing import Optional
from config import DB_NAME
import logging


logger = logging.getLogger(__name__)


def get_group_composition(user_username: str) -> Optional[list[dict]]:
    """Находит все группы пользователя и возвращает их состав"""
    try:
        if not user_username:
            return None

        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            groups_data = []

            # Ищем группы, где пользователь является админом
            cursor.execute("""
                SELECT id, name, admin, interns 
                FROM Groups
                WHERE admin = ?
            """, (user_username.lower(),))
            admin_groups = cursor.fetchall()

            # Ищем группы, где пользователь является стажёром
            cursor.execute("""
                SELECT id, name, admin, interns 
                FROM Groups
                WHERE interns LIKE ? OR interns LIKE ? OR interns = ?
            """, (
                f"{user_username.lower()} %",
                f"% {user_username.lower()}",
                user_username.lower()
            ))
            intern_groups = cursor.fetchall()

            # Объединяем все группы пользователя
            all_groups = admin_groups + intern_groups

            if not all_groups:
                return None

            for group in all_groups:
                # Получаем информацию об админе группы
                cursor.execute("""
                    SELECT surname, name, middle_name 
                    FROM Users 
                    WHERE username = ?
                """, (group['admin'],))
                admin = cursor.fetchone()

                if not admin:
                    continue

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

                groups_data.append({
                    'group_id': group['id'],
                    'group_name': group['name'],
                    'admin_info': admin_info,
                    'interns_info': interns_info,
                    'current_user_in_group': True
                })

            return groups_data

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None