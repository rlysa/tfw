from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_request.list_tasks import list_tasks


def list_of_tasks_kb(intern_username):
    """
    Создает инлайн-клавиатуру со списком задач стажёра
    :param intern_username: username стажера
    :return: InlineKeyboardMarkup
    """
    tasks = list_tasks(intern_username)

    if not tasks:
        return None

    buttons = []
    for task in tasks:
        task_id, title, _, status, deadline = task

        status_emoji = {
            'new': '🆕',
            'in_progress': '🔄',
            'completed': '✅',
            'overdue': '⏰'
        }.get(status, '')

        button_text = f"{status_emoji} {title} (до {deadline})"
        buttons.append([InlineKeyboardButton(
            text=button_text,
            callback_data=f"view_task_{task_id}"
        )])

    buttons.append([InlineKeyboardButton(
        text="Назад в главное меню",
        callback_data="back_to_intern_main"
    )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)