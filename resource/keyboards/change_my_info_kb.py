from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_edit_select_kb() -> InlineKeyboardMarkup:
    """Клавиатура выбора поля для редактирования"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Фамилия", callback_data="edit_surname"),
                InlineKeyboardButton(text="Имя", callback_data="edit_name"),
                InlineKeyboardButton(text="Отчество", callback_data="edit_middlename")
            ],
            [
                InlineKeyboardButton(text="Резюме", callback_data="edit_resume"),
                InlineKeyboardButton(text="Навыки", callback_data="edit_skills")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_info")
            ]
        ]
    )

def get_back_to_info_kb() -> InlineKeyboardMarkup:
    """Клавиатура для возврата к информации"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Отменить редактирование",
                    callback_data="back_to_info"
                )
            ]
        ]
    )