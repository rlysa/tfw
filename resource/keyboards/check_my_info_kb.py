from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_my_info_kb() -> InlineKeyboardMarkup:
    """Клавиатура для управления просмотром информации о себе"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 В меню",
                    callback_data="back_to_menu"
                )
            ]
        ]
    )