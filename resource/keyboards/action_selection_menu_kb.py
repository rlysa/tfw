from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_action_selection_menu() -> InlineKeyboardMarkup:
    """Главное меню с кнопкой просмотра группы"""
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
                    callback_data="show_my_group"  # Добавлена кнопка просмотра группы
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