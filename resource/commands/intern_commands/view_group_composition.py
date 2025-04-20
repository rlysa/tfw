from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.db_request.group_composition import get_group_composition
from resource.keyboards.group_composition_kb import get_group_composition_kb
from ..forms import Form
import logging


router = Router(name="view_group_composition_router")
logger = logging.getLogger(__name__)


def format_group_message(group_data: dict) -> str:
    """Форматирует информацию о группе"""
    message = [
        f"👥 Группа: {group_data['group_name']}",
        f"👨‍💼 Руководитель: {group_data['admin_info']['full_name']} (@{group_data['admin_info']['username']})",
        "",
        "📌 Стажёры в группе:"
    ]

    for i, intern in enumerate(group_data['interns_info'], 1):
        message.append(f"{i}. {intern['full_name']} (@{intern['username']})")

    if not group_data['interns_info']:
        message.append("Других стажёров в группе нет")

    return "\n".join(message)


async def show_user_group(callback: CallbackQuery, state: FSMContext):
    """Отображает группу пользователя"""
    try:
        username = callback.from_user.username
        if not username:
            await callback.answer("❌ У вас не установлен username", show_alert=True)
            return

        group_data = get_group_composition(username)
        if not group_data:
            await callback.answer("ℹ️ Вы не состоите ни в одной группе", show_alert=True)
            return

        await callback.message.edit_text(
            text=format_group_message(group_data),
            reply_markup=get_group_composition_kb()
        )
        await state.set_state(Form.view_group_composition)

    except Exception as e:
        logger.error(f"Ошибка при показе группы: {e}")
        await callback.answer("⚠️ Ошибка при загрузке группы", show_alert=True)


@router.callback_query(F.data == "show_my_group")
async def handle_show_my_group(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Моя группа'"""
    await show_user_group(callback, state)