from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_request.list_tasks import list_tasks


def list_of_tasks_kb(username: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру со списком задач
    без кнопки 'Назад', только с кнопкой 'Обновить'
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

    # Всегда добавляем кнопку обновления
    buttons.append([
        InlineKeyboardButton(
            text="🔄 Обновить список",
            callback_data="refresh_tasks"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)