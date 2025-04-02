import sqlite3
from typing import Dict, Optional
from config import DB_NAME
import logging

logger = logging.getLogger(__name__)


def get_group_composition(username: str) -> Optional[Dict]:
    """
    Находит группу пользователя и возвращает её состав
    (переименовано из get_user_group для соответствия импортам)
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, admin, interns FROM Groups")
            groups = cursor.fetchall()

            for group in groups:
                interns = group['interns'] or ""
                if username in [u.strip() for u in interns.split(',')]:
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

                    interns_info = []
                    for intern_username in [u.strip() for u in interns.split(',') if u.strip()]:
                        if intern_username == username:
                            continue

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

            return None

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None