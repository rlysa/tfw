from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_action_selection_menu() -> InlineKeyboardMarkup:
    """Создает клавиатуру главного меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Мои задачи",
                    callback_data="show_my_tasks"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👥 Моя группа",
                    callback_data="show_my_group"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Моя информация",
                    callback_data="show_my_info"
                )
            ]
        ]
    )