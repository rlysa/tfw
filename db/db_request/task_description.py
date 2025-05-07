import sqlite3
from typing import Optional, Tuple, List, Dict, Union
from config import DB_NAME
import logging
import json

logger = logging.getLogger(__name__)


def get_task_description(task_id: int) -> Optional[Tuple[str, str, str, str]]:
    """Получает описание задачи по ID"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, description, deadline, done 
                FROM Tasks 
                WHERE id = ?
            """, (task_id,))
            task = cursor.fetchone()
            if task:
                name, description, deadline, done = task
                status = "✅ Завершена" if done else "🔄 В работе"
                return name, description, deadline, status
            return None
    except sqlite3.Error as e:
        logger.error(f"Ошибка получения задачи: {e}")
        return None


def get_full_report(task_id: int) -> Optional[List[Dict]]:
    """Получает полные данные отчета"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT report FROM Tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            if result and result[0]:
                return json.loads(result[0])
            return None
    except (sqlite3.Error, json.JSONDecodeError) as e:
        logger.error(f"Ошибка получения отчета: {e}")
        return None


def has_any_reports(task_id: int) -> bool:
    """Проверяет наличие отчетов"""
    return bool(get_full_report(task_id))


def format_report_text(report_data: List[Dict]) -> str:
    """Форматирует отчет для отображения"""
    if not report_data:
        return "Отчеты отсутствуют"

    text_parts = ["📋 Полная история отчетов:"]
    for entry in report_data:
        if entry.get('type') == 'text':
            text_parts.append(
                f"\n📝 Текст от {entry.get('timestamp', 'N/A')}:\n"
                f"{entry.get('content', '')}"
            )
        elif entry.get('type') == 'file':
            file_type = {
                'document': 'Документ',
                'photo': 'Фото',
                'video': 'Видео',
                'audio': 'Аудио'
            }.get(entry.get('file_type'), entry.get('file_type', 'Файл'))

            text_parts.append(
                f"\n📁 {file_type} от {entry.get('timestamp', 'N/A')}"
            )

    return "\n".join(text_parts) if len(text_parts) > 1 else "Нет данных в отчете"


def change_task_status(task_id: int) -> bool:
    """Изменяет статус задачи"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT done FROM Tasks WHERE id = ?", (task_id,))
            current_status = cursor.fetchone()[0]
            new_status = not current_status
            cursor.execute(
                "UPDATE Tasks SET done = ? WHERE id = ?",
                (new_status, task_id)
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        logger.error(f"Ошибка изменения статуса: {e}")
        return False