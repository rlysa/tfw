from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_group_composition_kb() -> InlineKeyboardMarkup:
    """Клавиатура для управления просмотром группы (одиночная группа)"""
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


def get_group_selection_kb(total_groups: int, current_index: int) -> InlineKeyboardMarkup:
    """Клавиатура для выбора между несколькими группами"""
    buttons = [
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="group_prev"
            ),
            InlineKeyboardButton(
                text=f"{current_index + 1}/{total_groups}",
                callback_data="group_info"
            ),
            InlineKeyboardButton(
                text="Вперёд ➡️",
                callback_data="group_next"
            )
        ],
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
    return InlineKeyboardMarkup(inline_keyboard=buttons)