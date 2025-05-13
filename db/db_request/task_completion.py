import sqlite3
from datetime import datetime
from config import DB_NAME
import logging
import json

logger = logging.getLogger(__name__)


def save_text_report(task_id: int, user_id: int, text: str) -> bool:
    """Сохраняет текстовый отчет с инициализацией JSON"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            # Проверка типа задачи
            cursor.execute("SELECT report FROM Tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            if not result or result[0] != 'message':
                logger.error("Текстовые отчеты не разрешены для этой задачи")
                return False

            # Получение и инициализация отчетов
            cursor.execute("SELECT report FROM Tasks WHERE id = ?", (task_id,))
            report_json = cursor.fetchone()[0] or '[]'

            try:
                report_data = json.loads(report_json)
            except json.JSONDecodeError:
                report_data = []

            # Создание новой записи
            new_entry = {
                'type': 'text',
                'timestamp': datetime.now().strftime("%d.%m.%Y %H:%M"),
                'content': text,
                'user_id': user_id
            }
            report_data.append(new_entry)

            # Обновление данных
            cursor.execute(
                "UPDATE Tasks SET report = ? WHERE id = ?",
                (json.dumps(report_data, ensure_ascii=False), task_id)
            )
            conn.commit()
            return True

    except Exception as e:
        logger.error(f"Ошибка сохранения текста: {e}", exc_info=True)
        return False


def save_file_report(task_id: int, user_id: int, file_id: str, file_type: str) -> bool:
    """Сохраняет файловый отчет с инициализацией JSON"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            # Проверка типа задачи
            cursor.execute("SELECT report FROM Tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            if not result or result[0] != 'file':
                logger.error("Файловые отчеты не разрешены для этой задачи")
                return False

            # Получение и инициализация отчетов
            cursor.execute("SELECT report FROM Tasks WHERE id = ?", (task_id,))
            report_json = cursor.fetchone()[0] or '[]'

            try:
                report_data = json.loads(report_json)
            except json.JSONDecodeError:
                report_data = []

            # Создание новой записи
            new_entry = {
                'type': 'file',
                'timestamp': datetime.now().strftime("%d.%m.%Y %H:%M"),
                'file_id': file_id,
                'file_type': file_type,
                'user_id': user_id
            }
            report_data.append(new_entry)

            # Обновление данных
            cursor.execute(
                "UPDATE Tasks SET report = ? WHERE id = ?",
                (json.dumps(report_data, ensure_ascii=False), task_id)
            )
            conn.commit()
            return True

    except Exception as e:
        logger.error(f"Ошибка сохранения файла: {e}", exc_info=True)
        return False