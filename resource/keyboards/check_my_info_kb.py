from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_my_info_kb() -> InlineKeyboardMarkup:
    """Клавиатура для просмотра информации"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Изменить данные",
                    callback_data="change_my_info"
                ),
                InlineKeyboardButton(
                    text="Резюме",
                    callback_data="resume"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👥 Моя группа",
                    callback_data="show_my_group"
                ),
                InlineKeyboardButton(
                    text="🔙 В меню",
                    callback_data="back_to_menu"
                )
            ]
        ]
    )