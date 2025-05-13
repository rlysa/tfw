
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.db_request.check_my_info import get_full_user_info
from resource.keyboards.check_my_info_kb import get_my_info_kb
from resource.commands.forms import Form
import logging


router = Router(name="view_check_my_info_router")
logger = logging.getLogger(__name__)


def format_complete_user_info(user_data: dict) -> str:
    """Форматирует информацию о пользователе"""
    role_map = {
        1: "👑 Главный администратор",
        2: "👨‍💼 Администратор",
        3: "👨‍🎓 Стажёр"
    }

    message = [
        "👤 Ваша информация:",
        "",
        f"📛 ФИО: {user_data['surname']} {user_data['name']} {user_data['middle_name']}",
        f"🔹 Логин: @{user_data['username']}",
        f"👔 Роль: {role_map.get(user_data['role'], 'Неизвестно')}",
    ]

    if user_data.get('skills'):
        message.append(f"🛠 Навыки: {user_data['skills']}")
    if user_data.get('intern_skills'):
        message.append(f"🔧 Доп. навыки: {user_data['intern_skills']}")

    return "\n".join(message)


async def show_user_info(callback: CallbackQuery, state: FSMContext):
    """Отображает информацию о пользователе"""
    try:
        username = callback.from_user.username
        if not username:
            await callback.answer("❌ У вас не установлен username", show_alert=True)
            return

        user_data = get_full_user_info(username)
        if not user_data:
            await callback.answer("ℹ️ Ваш профиль не найден", show_alert=True)
            return

        await callback.message.edit_text(
            text=format_complete_user_info(user_data),
            reply_markup=get_my_info_kb()
        )

    except Exception as e:
        logger.error(f"Ошибка при показе информации: {e}")
        await callback.answer("⚠️ Ошибка при загрузке данных", show_alert=True)


@router.callback_query(F.data == "show_my_info")
async def handle_show_my_info(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Моя информация'"""
    await show_user_info(callback, state)