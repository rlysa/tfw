from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from resource.keyboards.list_of_tasks_kb import list_of_tasks_kb
from ..forms import Form
import logging
from datetime import datetime
from resource.keyboards.action_selection_menu_kb import get_action_selection_menu


router = Router(name="view_the_task_list_router")
logger = logging.getLogger(__name__)


@router.message(Command("tasks"))
async def handle_tasks_command(message: Message, state: FSMContext):
    """Обработчик команды /tasks"""
    try:
        username = message.from_user.username
        logger.info(f"User {username} requested tasks")

        keyboard = list_of_tasks_kb(username)

        if not keyboard or not keyboard.inline_keyboard:
            await message.answer("🎉 У вас пока нет активных задач")
            return

        await message.answer(
            f"📋 Список задач (обновлено: {datetime.now().strftime('%H:%M:%S')})",
            reply_markup=keyboard
        )
        await state.set_state(Form.view_the_task_list)

    except Exception as e:
        logger.error(f"Error in /tasks command: {e}")
        await message.answer("⚠️ Ошибка при загрузке задач")


@router.callback_query(F.data == "refresh_tasks")
async def handle_refresh_tasks(callback: CallbackQuery, state: FSMContext):
    """Обработчик обновления списка задач"""
    try:
        username = callback.from_user.username
        keyboard = list_of_tasks_kb(username)

        if not keyboard or not keyboard.inline_keyboard:
            await callback.message.edit_text(
                f"🎉 Нет активных задач (обновлено: {datetime.now().strftime('%H:%M:%S')})"
            )
        else:
            await callback.message.edit_text(
                f"📋 Список задач (обновлено: {datetime.now().strftime('%H:%M:%S')})",
                reply_markup=keyboard
            )

        await callback.answer("✅ Список обновлен")

    except Exception as e:
        logger.error(f"Error refreshing tasks: {e}")
        await callback.answer("⚠️ Ошибка при обновлении")

@router.callback_query(F.data == "back_to_menu")
async def handle_back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Назад в меню'"""
    try:
        await callback.message.edit_text(
            "📌 Главное меню\nВыберите действие:",
            reply_markup=get_action_selection_menu()
        )
        await state.set_state(Form.main_menu)
        await callback.answer()
    except Exception as e:
        logger.error(f"Error returning to menu: {e}")
        await callback.answer("⚠️ Ошибка при возврате в меню")