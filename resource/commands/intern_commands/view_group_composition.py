from typing import Dict
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.db_request.group_composition import get_group_composition  # Используем правильное имя
from resource.keyboards.group_composition_kb import get_group_composition_kb
from ..forms import Form
import logging

router = Router(name="view_group_composition_router")
logger = logging.getLogger(__name__)


def format_group_message(group_data: Dict) -> str:
    """Форматирует сообщение с информацией о группе"""
    message = [
        f"👥 <b>Группа:</b> {group_data['group_name']}",
        f"👨‍💼 <b>Руководитель:</b> {group_data['admin_info']['full_name']} (@{group_data['admin_info']['username']})",
        "",
        "📌 <b>Стажёры в группе:</b>"
    ]

    for i, intern in enumerate(group_data['interns_info'], 1):
        message.append(f"{i}. {intern['full_name']} (@{intern['username']})")

    if not group_data['interns_info']:
        message.append("Других стажёров в группе нет")

    return "\n".join(message)


async def show_user_group(message: Message, state: FSMContext):
    """Функция для отображения группы пользователя"""
    try:
        username = message.from_user.username
        group_data = get_group_composition(username)  # Используем переименованную функцию

        if not group_data or not group_data['current_user_in_group']:
            await message.answer("ℹ️ Вы не состоите ни в одной группе")
            return

        await message.answer(
            text=format_group_message(group_data),
            reply_markup=get_group_composition_kb()
        )
        await state.set_state(Form.view_group_composition)

    except Exception as e:
        logger.error(f"Error showing group: {e}")
        await message.answer("⚠️ Ошибка при загрузке группы")


@router.callback_query(F.data == "show_my_group")
async def handle_show_my_group(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Моя группа'"""
    await show_user_group(callback.message, state)
    await callback.answer()


@router.message(Command("my_group"))
async def handle_my_group_command(message: Message, state: FSMContext):
    """Обработчик команды /my_group"""
    await show_user_group(message, state)