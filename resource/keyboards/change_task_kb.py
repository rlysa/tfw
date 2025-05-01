from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


tasks_ibuttons = [
    [InlineKeyboardButton(text='Изменить', callback_data='change')],
    [InlineKeyboardButton(text='Удалить', callback_data='delete')],
    [InlineKeyboardButton(text='Меню команд', callback_data='back')]
]
tasks_ikeyboard = InlineKeyboardMarkup(inline_keyboard=tasks_ibuttons)

change_task_buttons = [
    [InlineKeyboardButton(text='Изменить название', callback_data='name')],
    [InlineKeyboardButton(text='Изменить список стажеров', callback_data='interns')],
    [InlineKeyboardButton(text='Изменить дедлайн', callback_data='deadline')],
    [InlineKeyboardButton(text='Изменить описание', callback_data='description')],
    [InlineKeyboardButton(text='Изменить формат отчета', callback_data='report')],
    [InlineKeyboardButton(text='Меню команд', callback_data='back')]
]
change_task_ikb = InlineKeyboardMarkup(inline_keyboard=change_task_buttons)

report_format_buttons = [
    [InlineKeyboardButton(text='Без отчета', callback_data='no_report')],
    [InlineKeyboardButton(text='Сообщение', callback_data='message')],
    [InlineKeyboardButton(text='Файл', callback_data='file')],
    [InlineKeyboardButton(text='Меню команд', callback_data='back')]
]

report_format_ikb = InlineKeyboardMarkup(inline_keyboard=report_format_buttons)
