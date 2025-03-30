from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_request.list_tasks import list_tasks


def list_of_tasks_kb(username: str) -> InlineKeyboardMarkup:
    tasks = list_tasks(username)
    if not tasks:
        return None

    buttons = []
    for task in tasks:
        task_id, title, _, status, deadline = task

        status_text = {
            'new': '🆕 Новая',
            'in_progress': '🔄 В работе',
            'completed': '✅ Завершена',
            'overdue': '⏰ Просрочена'
        }.get(status, '❓ Неизвестно')

        buttons.append([
            InlineKeyboardButton(
                text=f"{status_text} | {title} | До {deadline}",
                callback_data=f"view_task_{task_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🔄 Обновить список",
            callback_data="refresh_tasks"
        ),
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_main"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)