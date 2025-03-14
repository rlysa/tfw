from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.db_request.list_interns import list_of_interns


def list_of_interns_kb(admin):
    buttons = [[InlineKeyboardButton(text=i[0], callback_data=i[1])] for i in list_of_interns(admin)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
