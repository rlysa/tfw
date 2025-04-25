from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.db_request.group_composition import get_group_composition
from resource.keyboards.list_of_tasks_kb import list_of_tasks_kb  # Добавлен импорт
from resource.keyboards.action_selection_menu_kb import get_action_selection_menu
from resource.keyboards.group_composition_kb import get_group_composition_kb
from ..forms import Form
import logging


router = Router(name="action_selection_menu_router")
logger = logging.getLogger(__name__)


@router.message(Command("menu"))
async def show_main_menu(message: Message, state: FSMContext):
    """Показ главного меню"""
    try:
        await message.answer(
            "📌 Главное меню\nВыберите действие:",
            reply_markup=get_action_selection_menu()
        )
        await state.set_state(Form.main_menu)
    except Exception as e:
        logger.error(f"Error showing menu: {e}")
        await message.answer("⚠️ Ошибка при загрузке меню")


@router.callback_query(F.data == "show_my_tasks")
async def handle_show_my_tasks(callback: CallbackQuery, state: FSMContext):
    """Обработка кнопки 'Мои задачи'"""
    try:
        username = callback.from_user.username
        keyboard = list_of_tasks_kb(username)

        if not keyboard or not keyboard.inline_keyboard:
            await callback.message.edit_text("🎉 У вас пока нет активных задач")
        else:
            await callback.message.edit_text(
                "📋 Список ваших задач:",
                reply_markup=keyboard
            )
        await state.set_state(Form.view_the_task_list)
        await callback.answer()
    except Exception as e:
        logger.error(f"Error showing tasks: {e}")
        await callback.answer("⚠️ Ошибка при загрузке задач")


@router.callback_query(F.data == "show_my_group")
async def handle_show_my_group(callback: CallbackQuery, state: FSMContext):
    """Обработка кнопки 'Моя группа'"""
    try:
        username = callback.from_user.username
        group_data = get_group_composition(username)

        if not group_data or not group_data['current_user_in_group']:
            await callback.answer("ℹ️ Вы не состоите ни в одной группе")
            return

        await callback.message.edit_text(
            text=f"👥 Группа: {group_data['group_name']}\n"
                 f"👨‍💼 Руководитель: {group_data['admin_info']['full_name']}\n"
                 "📌 Стажёры:\n" +
                 "\n".join([f"{i}. {i['full_name']}" for i in group_data['interns_info']]),
            reply_markup=get_group_composition_kb()
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Error showing group: {e}")
        await callback.answer("⚠️ Ошибка при загрузке группы")