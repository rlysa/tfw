from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_task_description_kb(task_id: int, is_done: bool, report_type: str, has_reports: bool) -> InlineKeyboardMarkup:
    """Клавиатура управления задачей"""
    buttons = []

    if not is_done:
        buttons.append([
            InlineKeyboardButton(
                text="✅ Завершить",
                callback_data=f"change_status_{task_id}"
            )
        ])
    else:
        if report_type != 'no_report':
            buttons.append([
                InlineKeyboardButton(
                    text="📝 Управление отчетами",
                    callback_data=f"report_options_{task_id}"
                )
            ])

            if has_reports:
                buttons.append([
                    InlineKeyboardButton(
                        text="📤 Просмотреть отчеты",
                        callback_data=f"view_report_{task_id}"
                    )
                ])

    buttons.append([
        InlineKeyboardButton(
            text="🔙 Назад к списку",
            callback_data="back_to_tasks_list"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_report_options_kb(task_id: int, report_type: str) -> InlineKeyboardMarkup:
    """Клавиатура выбора типа отчета"""
    buttons = []

    if report_type == 'message':
        buttons.append([
            InlineKeyboardButton(
                text="📝 Добавить текстовый отчет",
                callback_data=f"text_report_{task_id}"
            )
        ])
    elif report_type == 'file':
        buttons.append([
            InlineKeyboardButton(
                text="📁 Прикрепить файл",
                callback_data=f"file_report_{task_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🔙 Назад к задаче",
            callback_data=f"view_task_{task_id}"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)