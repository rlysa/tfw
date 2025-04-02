from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.db_request.group_composition import get_group_composition
from resource.keyboards.action_selection_menu_kb import get_action_selection_menu
from ..forms import Form
import logging

router = Router(name="action_selection_menu_router")
logger = logging.getLogger(__name__)


@router.message(Command("menu"))
async def show_main_menu(message: Message, state: FSMContext):
    await message.answer(
        "📌 <b>Главное меню</b>\nВыберите действие:",
        reply_markup=get_action_selection_menu()
    )
    await state.set_state(Form.main_menu)


@router.callback_query(F.data == "show_my_group")
async def handle_show_my_group(callback: CallbackQuery, state: FSMContext):
    try:
        username = callback.from_user.username
        group_data = get_group_composition(username)  # Используем переименованную функцию

        if not group_data or not group_data['current_user_in_group']:
            await callback.answer("ℹ️ Вы не состоите ни в одной группе")
            return

        await callback.message.edit_text(
            text=f"👥 <b>Группа:</b> {group_data['group_name']}\n"
                 f"👨‍💼 <b>Руководитель:</b> {group_data['admin_info']['full_name']}\n"
                 "📌 <b>Стажёры:</b>\n" +
                 "\n".join([f"{i}. {i['full_name']}" for i in group_data['interns_info']]),
            reply_markup=get_group_composition_kb()
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Error showing group: {e}")
        await callback.answer("⚠️ Ошибка при загрузке группы")