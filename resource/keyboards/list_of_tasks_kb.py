from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_request.list_tasks import list_tasks

def list_of_tasks_kb(username: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру со списком задач и кнопкой "Назад в меню"
    """
    tasks = list_tasks(username)
    buttons = []

    if tasks:
        for task in tasks:
            task_id, name, _, status, deadline = task
            status_text = {
                'completed': '✅ Завершена',
                'in_progress': '🔄 В работе'
            }.get(status, '❓ Неизвестно')

            buttons.append([
                InlineKeyboardButton(
                    text=f"{status_text} | {name} | До {deadline}",
                    callback_data=f"view_task_{task_id}"
                )
            ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text="🎉 Нет активных задач",
                callback_data="no_tasks"
            )
        ])

    # Кнопки управления (Обновить и Назад)
    buttons.append([
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_tasks"),
        InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)