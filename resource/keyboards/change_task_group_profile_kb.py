from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


change_delete_buttons = [
    [InlineKeyboardButton(text='Изменить', callback_data='change')],
    [InlineKeyboardButton(text='Удалить', callback_data='delete')],
    [InlineKeyboardButton(text='Меню команд', callback_data='back')]
]
change_delete_ikb = InlineKeyboardMarkup(inline_keyboard=change_delete_buttons)

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

change_group_buttons = [
    [InlineKeyboardButton(text='Изменить название', callback_data='name')],
    [InlineKeyboardButton(text='Изменить список стажеров', callback_data='interns')],
    [InlineKeyboardButton(text='Меню команд', callback_data='back')]
]
change_group_ikb = InlineKeyboardMarkup(inline_keyboard=change_group_buttons)

change_profile_buttons = [
    [InlineKeyboardButton(text='Изменить', callback_data='change')],
    [InlineKeyboardButton(text='Меню команд', callback_data='back')]
]
change_profile_ikb = InlineKeyboardMarkup(inline_keyboard=change_profile_buttons)

what_change_profile_buttons = [
    [InlineKeyboardButton(text='Изменить фамилию', callback_data='surname')],
    [InlineKeyboardButton(text='Изменить имя', callback_data='name')],
    [InlineKeyboardButton(text='Изменить отчество', callback_data='middle_name')]
]
what_change_profile_ikb = InlineKeyboardMarkup(inline_keyboard=what_change_profile_buttons)
