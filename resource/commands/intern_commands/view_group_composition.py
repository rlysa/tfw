from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.db_request.group_composition import get_group_composition
from resource.keyboards.group_composition_kb import get_group_composition_kb, get_group_selection_kb
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


async def show_user_group(callback: CallbackQuery, state: FSMContext, group_index: int = 0):
    """Отображает группу пользователя"""
    try:
        username = callback.from_user.username
        if not username:
            await callback.answer("❌ У вас не установлен username", show_alert=True)
            return

        groups_data = get_group_composition(username)
        if not groups_data:
            await callback.answer("ℹ️ Вы не состоите ни в одной группе", show_alert=True)
            return

        await state.update_data(all_groups=groups_data, current_group_index=group_index)

        if len(groups_data) > 1:
            await callback.message.edit_text(
                text=format_group_message(groups_data[group_index]),
                reply_markup=get_group_selection_kb(len(groups_data), group_index)
            )
        else:
            await callback.message.edit_text(
                text=format_group_message(groups_data[0]),
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


@router.callback_query(F.data.startswith("group_"))
async def handle_group_selection(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора группы"""
    action = callback.data.split("_")[1]

    data = await state.get_data()
    groups_data = data.get('all_groups', [])
    current_index = data.get('current_group_index', 0)

    if not groups_data:
        await callback.answer("ℹ️ Нет данных о группах", show_alert=True)
        return

    if action == "next":
        new_index = (current_index + 1) % len(groups_data)
    elif action == "prev":
        new_index = (current_index - 1) % len(groups_data)
    else:
        try:
            new_index = int(action)
        except ValueError:
            new_index = current_index

    await show_user_group(callback, state, new_index)