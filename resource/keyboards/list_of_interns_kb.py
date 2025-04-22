from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_request.list_interns import list_of_interns


def list_of_interns_kb(admin):
    buttons = [[InlineKeyboardButton(text=i[0], callback_data=i[1])] for i in list_of_interns(admin)]
    buttons.append([InlineKeyboardButton(text='Меню команд', callback_data='back')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def list_of_interns_select_kb(admin, selected):
    buttons = []
    for i in list_of_interns(admin):
        if i[1] in selected:
            buttons.append([InlineKeyboardButton(text=f'\U00002705 {i[0]}', callback_data=i[1])])
        else:
            buttons.append([InlineKeyboardButton(text=i[0], callback_data=i[1])])
    buttons.append([InlineKeyboardButton(text='Далее', callback_data='next')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
