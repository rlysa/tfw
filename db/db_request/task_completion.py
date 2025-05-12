import sqlite3
from datetime import datetime
from config import DB_NAME
import logging
import json

logger = logging.getLogger(__name__)


def save_text_report(task_id: int, user_id: int, text: str) -> bool:
    """Сохраняет текстовый отчет"""
    try:
        new_entry = {
            'type': 'text',
            'timestamp': datetime.now().strftime("%d.%m.%Y %H:%M"),
            'content': text,
            'user_id': user_id
        }

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT done FROM Tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()

            report_data = []
            if result and result[0]:
                try:
                    report_data = json.loads(result[0])
                except json.JSONDecodeError:
                    logger.error("Ошибка декодирования JSON, создаем новый отчет")

            if not isinstance(report_data, list):
                report_data = []

            report_data.append(new_entry)

            cursor.execute(
                "UPDATE Tasks SET done = ? WHERE id = ?",
                (json.dumps(report_data), task_id)
            )
            conn.commit()
            return True
    except Exception as e:
        logger.error(f"Ошибка сохранения текста: {e}")
        return False


def save_file_report(task_id: int, user_id: int, file_id: str, file_type: str) -> bool:
    """Сохраняет файловый отчет"""
    try:
        new_entry = {
            'type': 'file',
            'timestamp': datetime.now().strftime("%d.%m.%Y %H:%M"),
            'file_id': file_id,
            'file_type': file_type,
            'user_id': user_id
        }

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT done FROM Tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()

            report_data = []
            if result and result[0]:
                try:
                    report_data = json.loads(result[0])
                except json.JSONDecodeError:
                    logger.error("Ошибка декодирования JSON, создаем новый отчет")

            if not isinstance(report_data, list):
                report_data = []

            report_data.append(new_entry)

            cursor.execute(
                "UPDATE Tasks SET done = ? WHERE id = ?",
                (json.dumps(report_data), task_id)
            )
            conn.commit()
            return True
    except Exception as e:
        logger.error(f"Ошибка сохранения файла: {e}")
        return False