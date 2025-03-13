from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

buttons = [
    [KeyboardButton(text='Стажеры'), KeyboardButton(text='Группы')]
]

admin_keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                     resize_keyboard=True,
                                     one_time_keyboard=True)
