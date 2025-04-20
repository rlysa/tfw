from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


button = [[KeyboardButton(text='Назад')]]
back_kb = ReplyKeyboardMarkup(keyboard=button,
                              resize_keyboard=True,
                              one_time_keyboard=True)