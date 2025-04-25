from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = [[InlineKeyboardButton(text='Принять', callback_data='accept'),
            InlineKeyboardButton(text='Отклонить', callback_data='reject')]]

accept_new_user_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
