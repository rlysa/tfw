# keyboards/task_description_kb.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_task_description_kb(task_id: int, is_done: bool) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления задачей
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="✅ Завершить" if not is_done else "🔄 Возобновить",
                callback_data=f"change_status_{task_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Отправить отчет",
                callback_data=f"report_options_{task_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад к списку",
                callback_data="back_to_tasks_list"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_report_options_kb(task_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора типа отчета
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="📝 Текстовый отчет",
                callback_data=f"text_report_{task_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📁 Файловый отчет",
                callback_data=f"file_report_{task_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад к задаче",
                callback_data=f"view_task_{task_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)