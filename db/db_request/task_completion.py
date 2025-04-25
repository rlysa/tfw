# db/db_request/task_completion.py
import sqlite3
from datetime import datetime
from config import DB_NAME
import logging

logger = logging.getLogger(__name__)


def save_text_report(task_id: int, user_id: int, text: str) -> bool:
    """Сохраняет текстовый отчет в таблицу Tasks"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            # Получаем текущий отчет (если есть)
            cursor.execute("SELECT report FROM Tasks WHERE id = ?", (task_id,))
            current_report = cursor.fetchone()[0] or ""

            # Формируем новый отчет с меткой времени
            new_report = f"{current_report}\n\n[{datetime.now().strftime('%d.%m.%Y %H:%M')}] {text}"

            # Обновляем запись
            cursor.execute(
                "UPDATE Tasks SET report = ? WHERE id = ?",
                (new_report.strip(), task_id)
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        logger.error(f"Ошибка БД при сохранении текстового отчета: {e}")
        return False


def save_file_report(task_id: int, user_id: int, file_id: str, file_type: str) -> bool:
    """Сохраняет информацию о файловом отчете в таблицу Tasks"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            # Получаем текущий отчет (если есть)
            cursor.execute("SELECT report FROM Tasks WHERE id = ?", (task_id,))
            current_report = cursor.fetchone()[0] or ""

            # Формируем запись о файле
            file_record = f"\n\n[{datetime.now().strftime('%d.%m.%Y %H:%M')}] Файл ({file_type}): {file_id}"

            # Обновляем запись
            cursor.execute(
                "UPDATE Tasks SET report = ? WHERE id = ?",
                (f"{current_report}{file_record}".strip(), task_id)
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        logger.error(f"Ошибка БД при сохранении файлового отчета: {e}")
        return False