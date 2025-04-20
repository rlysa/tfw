from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.db_request.list_groups import list_of_groups

def list_of_groups_kb(admin):
    buttons = [[InlineKeyboardButton(text=i[1], callback_data=f'{i[0]}')] for i in list_of_groups(admin)]
    buttons.append([InlineKeyboardButton(text='Меню команд', callback_data='back')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
