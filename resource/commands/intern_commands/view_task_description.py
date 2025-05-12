import aiogram
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from config import TOKEN
from db.db_request.task_description import get_task_description, change_task_status
from ...keyboards.task_description_kb import get_task_description_kb
from ...keyboards.list_of_tasks_kb import list_of_tasks_kb
import logging
from typing import Union

from db.db_request.task_description import (
    get_task_description,
    change_task_status,
    has_any_reports,
    get_full_report,
    format_report_text
)
from resource.keyboards.task_description_kb import get_task_description_kb
from resource.keyboards.list_of_tasks_kb import list_of_tasks_kb

router = Router(name="view_task_description_router")
logger = logging.getLogger(__name__)


async def show_task_description(message_or_callback: Union[Message, CallbackQuery], task_id: int):
    """Универсальная функция показа задачи"""
    try:
        if isinstance(message_or_callback, CallbackQuery):
            message = message_or_callback.message
            callback = message_or_callback
        else:
            message = message_or_callback
            callback = None

        task_info = get_task_description(task_id)
        if not task_info:
            await message.answer("⚠️ Задача не найдена")
            if callback:
                await callback.answer()
            return False

        name, description, deadline, status = task_info
        has_report = has_any_reports(task_id)

        message_text = (
            f"📌 {name}\n\n"
            f"📝 Описание:\n{description}\n\n"
            f"⏳ Срок выполнения: {deadline}\n"
            f"🔄 Статус: {status}"
        )

        keyboard = get_task_description_kb(task_id, status == "✅ Завершена", has_report)

        # Пытаемся редактировать, если возможно
        try:
            await message.edit_text(
                text=message_text,
                reply_markup=keyboard
            )
        except:
            # Если редактирование невозможно, отправляем новое сообщение
            await message.answer(
                text=message_text,
                reply_markup=keyboard
            )

        if callback:
            await callback.answer()
        return True
    except Exception as e:
        logger.error(f"Ошибка показа задачи: {e}")
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.answer("⚠️ Ошибка при отображении задачи")
        else:
            await message_or_callback.answer("⚠️ Произошла ошибка при отображении задачи")
        return False


@router.callback_query(F.data.startswith("view_report_"))
async def handle_view_report(callback: CallbackQuery):
    """Обработчик просмотра отчетов"""
    try:
        task_id = int(callback.data.split("_")[2])
        report_data = get_full_report(task_id)

        if not report_data:
            await callback.answer("ℹ️ Отчеты отсутствуют")
            return

        # Отправляем текстовую часть
        await callback.message.answer(
            format_report_text(report_data),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Назад к задаче",
                    callback_data=f"view_task_{task_id}"
                )
            ]])
        )

        # Отправляем файлы с правильными подписями
        for entry in report_data:
            if entry.get('type') == 'file':
                try:
                    file_type = {
                        'document': 'Документ',
                        'photo': 'Фото',
                        'video': 'Видео',
                        'audio': 'Аудио'
                    }.get(entry.get('file_type'), 'Файл')

                    caption = f"{file_type} от {entry.get('timestamp', 'N/A')}"

                    if entry.get('file_type') == 'document':
                        await callback.message.answer_document(
                            entry.get('file_id'),
                            caption=caption
                        )
                    elif entry.get('file_type') == 'photo':
                        await callback.message.answer_photo(
                            entry.get('file_id'),
                            caption=caption
                        )
                    elif entry.get('file_type') == 'video':
                        await callback.message.answer_video(
                            entry.get('file_id'),
                            caption=caption
                        )
                    elif entry.get('file_type') == 'audio':
                        await callback.message.answer_audio(
                            entry.get('file_id'),
                            caption=caption
                        )
                except Exception as e:
                    logger.error(f"Ошибка отправки файла: {e}")

        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка показа отчета: {e}")
        await callback.answer("⚠️ Ошибка при отображении отчета")


@router.callback_query(F.data.startswith("view_task_"))
async def handle_view_task(callback: CallbackQuery, state: FSMContext):
    """Обработчик просмотра задачи"""
    task_id = int(callback.data.split("_")[2])
    await show_task_description(callback, task_id)


@router.callback_query(F.data.startswith("change_status_"))
async def handle_change_status(callback: CallbackQuery, state: FSMContext):
    """Обработчик изменения статуса"""
    task_id = int(callback.data.split("_")[2])

    change_task_st = change_task_status(task_id)
    if change_task_st[0]:
        await show_task_description(callback.message, task_id)
        bot = Bot(TOKEN)
        await bot.send_message(chat_id=change_task_st[2], text=f'Задача "{change_task_st[1]}" выполнена')
        await bot.session.close()
        await callback.answer("Статус задачи обновлен!")
    else:
        await callback.answer("⚠️ Не удалось изменить статус")


@router.callback_query(F.data == "back_to_tasks_list")
async def handle_back_to_list(callback: CallbackQuery, state: FSMContext):
    """Обработчик возврата к списку задач"""
    try:
        username = callback.from_user.username
        keyboard = list_of_tasks_kb(username)

        # Всегда редактируем сообщение
        await callback.message.edit_text(
            "📋 Список задач:",
            reply_markup=keyboard
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка возврата к списку: {e}")
        await callback.answer("⚠️ Ошибка при возврате к списку задач")