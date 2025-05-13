from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from config import TOKEN
import logging
from typing import Union

from db.db_request.task_description import (
    get_task_description,
    change_task_status,
    has_any_reports,
    get_full_report,
    format_report_text
)
from ...keyboards.task_description_kb import get_task_description_kb, get_report_options_kb
from ...keyboards.list_of_tasks_kb import list_of_tasks_kb

router = Router(name="view_task_description_router")
logger = logging.getLogger(__name__)


async def show_task_description(message_or_callback: Union[Message, CallbackQuery], task_id: int):
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

        name, description, deadline, status, report_type = task_info
        is_done = status == "✅ Завершена"
        has_report = has_any_reports(task_id) and report_type != 'no_report'

        message_text = (
            f"📌 {name}\n\n"
            f"📝 Описание:\n{description}\n\n"
            f"⏳ Срок выполнения: {deadline}\n"
            f"🔄 Статус: {status}"
        )

        keyboard = get_task_description_kb(
            task_id=task_id,
            is_done=is_done,
            report_type=report_type,
            has_reports=has_report
        )

        try:
            await message.edit_text(
                text=message_text,
                reply_markup=keyboard
            )
        except:
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
    try:
        task_id = int(callback.data.split("_")[2])
        report_data = get_full_report(task_id)

        if not report_data:
            await callback.answer("ℹ️ Отчеты отсутствуют")
            return

        await callback.message.answer(
            format_report_text(report_data),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Назад к задаче",
                    callback_data=f"view_task_{task_id}"
                )
            ]])
        )

        for entry in report_data:
            if entry.get('type') == 'file':
                try:
                    file_type = entry.get('file_type', 'document')
                    caption = f"{file_type.capitalize()} от {entry.get('timestamp', 'N/A')}"

                    method = {
                        'document': callback.message.answer_document,
                        'photo': callback.message.answer_photo,
                        'video': callback.message.answer_video,
                        'audio': callback.message.answer_audio
                    }.get(file_type, callback.message.answer_document)

                    await method(entry['file_id'], caption=caption)
                except Exception as e:
                    logger.error(f"Ошибка отправки файла: {e}")

        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка показа отчета: {e}")
        await callback.answer("⚠️ Ошибка при отображении отчета")


@router.callback_query(F.data.startswith("report_options_"))
async def handle_report_options(callback: CallbackQuery):
    try:
        task_id = int(callback.data.split("_")[2])
        task_info = get_task_description(task_id)

        if not task_info:
            await callback.answer("⚠️ Задача не найдена")
            return

        report_type = task_info[4]
        keyboard = get_report_options_kb(task_id, report_type)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка обработки опций отчета: {e}")
        await callback.answer("⚠️ Ошибка при обработке запроса")


@router.callback_query(F.data.startswith("view_task_"))
async def handle_view_task(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split("_")[2])
    await show_task_description(callback, task_id)


@router.callback_query(F.data.startswith("change_status_"))
async def handle_change_status(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split("_")[2])
    result = change_task_status(task_id)

    if result[0]:
        bot = Bot(TOKEN)
        try:
            await bot.send_message(
                chat_id=result[2],
                text=f'Задача "{result[1]}" выполнена'
            )
            await show_task_description(callback.message, task_id)
        finally:
            await bot.session.close()
        await callback.answer("✅ Задача завершена")
    else:
        await callback.answer("⚠️ Не удалось завершить задачу")


@router.callback_query(F.data == "back_to_tasks_list")
async def handle_back_to_list(callback: CallbackQuery, state: FSMContext):
    try:
        username = callback.from_user.username
        keyboard = list_of_tasks_kb(username)
        await callback.message.edit_text(
            "📋 Список задач:",
            reply_markup=keyboard
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка возврата к списку: {e}")
        await callback.answer("⚠️ Ошибка при возврате к списку задач")