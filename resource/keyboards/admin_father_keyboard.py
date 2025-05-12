from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


buttons = [
    [KeyboardButton(text='Стажеры'), KeyboardButton(text='Администраторы')],
    [KeyboardButton(text='Профиль')]
]
admin_father_keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)
