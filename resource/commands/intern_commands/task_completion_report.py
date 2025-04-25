# intern_commands/task_completion_report.py
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
import logging

from db.db_request.task_completion import save_text_report, save_file_report
from keyboards.task_description_kb import get_report_options_kb, get_task_description_kb

router = Router(name="task_completion_report_router")
logger = logging.getLogger(__name__)

class ReportStates(aiogram.StatesGroup):
    waiting_text = aiogram.State()
    waiting_file = aiogram.State()

@router.callback_query(F.data.startswith("report_options_"))
async def show_report_options(callback: CallbackQuery):
    """Показывает варианты отправки отчета"""
    task_id = int(callback.data.split("_")[2])
    await callback.message.edit_text(
        text="📤 Выберите тип отчета:",
        reply_markup=get_report_options_kb(task_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("text_report_"))
async def start_text_report(callback: CallbackQuery, state: FSMContext):
    """Начало текстового отчета"""
    task_id = int(callback.data.split("_")[2])
    await state.set_state(ReportStates.waiting_text)
    await state.update_data(task_id=task_id)
    
    cancel_btn = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data=f"view_task_{task_id}")
    ]])
    
    await callback.message.edit_text(
        text="✍️ Введите текст отчета:",
        reply_markup=cancel_btn
    )
    await callback.answer()

@router.message(ReportStates.waiting_text)
async def process_text_report(message: Message, state: FSMContext):
    """Обрабатывает текстовый отчет"""
    data = await state.get_data()
    task_id = data.get("task_id")
    
    if save_text_report(task_id, message.from_user.id, message.text):
        await message.answer("✅ Текстовый отчет сохранен!")
    else:
        await message.answer("⚠️ Ошибка сохранения отчета")
    
    await state.clear()
    await show_task_description(message, task_id)

@router.callback_query(F.data.startswith("file_report_"))
async def start_file_report(callback: CallbackQuery, state: FSMContext):
    """Начало файлового отчета"""
    task_id = int(callback.data.split("_")[2])
    await state.set_state(ReportStates.waiting_file)
    await state.update_data(task_id=task_id)
    
    cancel_btn = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data=f"view_task_{task_id}")
    ]])
    
    await callback.message.edit_text(
        text="📎 Прикрепите файл (документ, фото, видео или аудио):",
        reply_markup=cancel_btn
    )
    await callback.answer()

@router.message(ReportStates.waiting_file, F.document | F.photo | F.video | F.audio)
async def process_file_report(message: Message, state: FSMContext):
    """Обрабатывает файловый отчет"""
    data = await state.get_data()
    task_id = data.get("task_id")
    
    if message.document:
        file_id = message.document.file_id
        file_type = "document"