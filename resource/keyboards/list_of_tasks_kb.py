from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from db.db_request.list_tasks import list_tasks, list_of_tasks


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


def list_of_tasks_admin_kb(admin):
    buttons = [[InlineKeyboardButton(text=i[1], callback_data=f'{i[0]}')] for i in list_of_tasks(admin)]
    buttons.append([InlineKeyboardButton(text='Меню команд', callback_data='back')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def tasks_commands(report, done):
    buttons = [[InlineKeyboardButton(text='Изменить', callback_data='change')],
               [InlineKeyboardButton(text='Удалить', callback_data='delete')],
               [InlineKeyboardButton(text='Меню команд', callback_data='back')]]
    if done:
        buttons.insert(2,
                       [InlineKeyboardButton(text='Вернуть на доработку', callback_data='return')])
        if report != 'Без отчета':
            buttons.insert(3,
                           [InlineKeyboardButton(text='Посмотреть отчет', callback_data='report')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
