from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import logging
from typing import Union

from db.db_request.task_completion import save_text_report, save_file_report
from resource.keyboards.task_description_kb import get_report_options_kb
from .view_task_description import show_task_description

router = Router(name="task_completion_report_router")
logger = logging.getLogger(__name__)


class ReportStates(StatesGroup):
    waiting_text = State()
    waiting_file = State()


@router.callback_query(F.data.startswith("report_options_"))
async def show_report_options(callback: CallbackQuery):
    """Показывает варианты отчетов"""
    try:
        task_id = int(callback.data.split("_")[2])
        await callback.message.edit_text(
            text="📤 Выберите тип отчета:",
            reply_markup=get_report_options_kb(task_id)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка показа вариантов отчетов: {e}")
        await callback.answer("⚠️ Ошибка при выборе типа отчета")


@router.callback_query(F.data.startswith("text_report_"))
async def start_text_report(callback: CallbackQuery, state: FSMContext):
    """Начинает ввод текстового отчета"""
    try:
        task_id = int(callback.data.split("_")[2])
        await state.set_state(ReportStates.waiting_text)
        await state.update_data(task_id=task_id)

        await callback.message.edit_text(
            text="✍️ Введите текст отчета:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data=f"view_task_{task_id}"
                )
            ]])
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка начала текстового отчета: {e}")
        await callback.answer("⚠️ Ошибка при начале ввода текста")


@router.message(ReportStates.waiting_text)
async def process_text_report(message: Message, state: FSMContext):
    """Обрабатывает текстовый отчет"""
    try:
        data = await state.get_data()
        task_id = data['task_id']

        if save_text_report(task_id, message.from_user.id, message.text):
            await message.answer("✅ Текст сохранен!")
            await state.clear()
            await show_task_description(message, task_id)
        else:
            await message.answer("⚠️ Ошибка сохранения")
            await state.clear()
    except Exception as e:
        logger.error(f"Ошибка обработки текста: {e}")
        await message.answer("⚠️ Ошибка при сохранении текста")
        await state.clear()


@router.callback_query(F.data.startswith("file_report_"))
async def start_file_report(callback: CallbackQuery, state: FSMContext):
    """Начинает загрузку файла"""
    try:
        task_id = int(callback.data.split("_")[2])
        await state.set_state(ReportStates.waiting_file)
        await state.update_data(task_id=task_id)

        await callback.message.edit_text(
            text="📎 Прикрепите файл (документ, фото, видео или аудио):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data=f"view_task_{task_id}"
                )
            ]])
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка начала загрузки файла: {e}")
        await callback.answer("⚠️ Ошибка при начале загрузки файла")


@router.message(ReportStates.waiting_file, F.document | F.photo | F.video | F.audio)
async def process_file_report(message: Message, state: FSMContext):
    """Обрабатывает прикрепленный файл"""
    try:
        data = await state.get_data()
        task_id = data['task_id']

        file_type = None
        file_id = None

        if message.document:
            file_id = message.document.file_id
            file_type = "document"
        elif message.photo:
            file_id = message.photo[-1].file_id
            file_type = "photo"
        elif message.video:
            file_id = message.video.file_id
            file_type = "video"
        elif message.audio:
            file_id = message.audio.file_id
            file_type = "audio"

        if file_id and file_type and save_file_report(task_id, message.from_user.id, file_id, file_type):
            file_type_name = {
                'document': 'Документ',
                'photo': 'Фото',
                'video': 'Видео',
                'audio': 'Аудио'
            }.get(file_type, 'Файл')

            await message.answer(f"✅ {file_type_name} сохранен!")
            await state.clear()
            await show_task_description(message, task_id)
        else:
            await message.answer("⚠️ Ошибка сохранения файла")
            await state.clear()
    except Exception as e:
        logger.error(f"Ошибка обработки файла: {e}")
        await message.answer("⚠️ Ошибка при сохранении файла")
        await state.clear()