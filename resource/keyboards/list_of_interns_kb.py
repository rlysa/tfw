from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_request.list_interns import list_of_interns
from db.db_request.list_admins import list_of_admins


def list_of_interns_kb(admin):
    buttons = [[InlineKeyboardButton(text=i[0], callback_data=i[1])] for i in list_of_interns(admin)]
    buttons.append([InlineKeyboardButton(text='Меню команд', callback_data='back')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def list_of_admins_kb():
    buttons = [[InlineKeyboardButton(text=i[0], callback_data=i[1])] for i in list_of_admins()]
    buttons.append([InlineKeyboardButton(text='Обновить ключи', callback_data='new_keys')])
    buttons.append([InlineKeyboardButton(text='Меню команд', callback_data='back')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def list_of_interns_select_kb(list_interns, selected):
    buttons = []
    for i in list_interns:
        if i[1] in selected:
            buttons.append([InlineKeyboardButton(text=f'\U00002705 {i[0]}', callback_data=i[1])])
        else:
            buttons.append([InlineKeyboardButton(text=i[0], callback_data=i[1])])
    buttons.append([InlineKeyboardButton(text='Далее', callback_data='next')])
    buttons.append([InlineKeyboardButton(text='Меню команд', callback_data='back')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def list_of_interns_selected_kb(list_interns, selected):
    buttons = [[InlineKeyboardButton(text=f'\U00002705 {i[0]}', callback_data=i[1])] for i in list_interns if i[1] in selected]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
