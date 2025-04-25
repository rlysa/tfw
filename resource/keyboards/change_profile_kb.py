from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

button = [[KeyboardButton(text='Изменить')],
          [KeyboardButton(text='Меню команд')]]

change_profile_keyboard = ReplyKeyboardMarkup(keyboard=button,
                                              one_time_keyboard=True,
                                              resize_keyboard=True)
