from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button = [[KeyboardButton(text='Назад')]]
back_kb = ReplyKeyboardMarkup(keyboard=button,
                              resize_keyboard=True) #,
                              # one_time_keyboard=True)

ibutton = [[InlineKeyboardButton(text='Назад', callback_data='back')]]
back_ikb = InlineKeyboardMarkup(inline_keyboard=ibutton)
