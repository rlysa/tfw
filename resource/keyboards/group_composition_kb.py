from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_group_composition_kb() -> InlineKeyboardMarkup:
    """Клавиатура для управления просмотром группы"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Обновить",
                    callback_data="refresh_group"
                ),
                InlineKeyboardButton(
                    text="🔙 В меню",
                    callback_data="back_to_menu"
                )
            ]
        ]
    )