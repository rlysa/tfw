from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_task_description_kb(task_id: int, is_done: bool) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления задачей

    Args:
        task_id: ID задачи
        is_done: Текущий статус выполнения

    Returns:
        InlineKeyboardMarkup с кнопками управления
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="✅ Завершить" if not is_done else "🔄 Возобновить",
                callback_data=f"change_status_{task_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Отправить отчет",
                callback_data=f"send_report_{task_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад к списку",
                callback_data="back_to_tasks_list"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)