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
    """Форматирует полную информацию о пользователе с навыками"""
    role_map = {
        1: "👑 Главный администратор",
        2: "👨‍💼 Администратор",
        3: "👨‍🎓 Стажёр"
    }

    message = [
        "👤 <b>ПОЛНАЯ ИНФОРМАЦИЯ</b>",
        "",
        f"📛 <b>ФИО:</b> {user_data.get('surname', '')} {user_data.get('name', '')} {user_data.get('middle_name', '')}",
        f"🔹 <b>Логин:</b> @{user_data.get('username', '')}",
        f"👔 <b>Роль:</b> {role_map.get(user_data.get('role'), 'Неизвестно')}",
    ]

    # Контактная информация
    if user_data.get('phone'):
        message.append(f"📱 <b>Телефон:</b> {user_data['phone']}")
    if user_data.get('email'):
        message.append(f"📧 <b>Email:</b> {user_data['email']}")

    # Навыки из Users
    if user_data.get('skills'):
        message.append(f"🛠 <b>Навыки:</b> {user_data['skills']}")

    # Навыки из Interns (если есть)
    if user_data.get('intern_skills'):
        message.append(f"🔧 <b>Навыки:</b> {user_data['intern_skills']}")

    return "\n".join(message)


async def show_complete_user_info(message: Message, state: FSMContext):
    try:
        username = message.from_user.username
        if not username:
            await message.answer("❌ У вас не установлен username в Telegram")
            return

        user_data = get_full_user_info(username)
        if not user_data:
            await message.answer("ℹ️ Ваш профиль не найден в системе")
            return

        await message.answer(
            text=format_complete_user_info(user_data),
            reply_markup=get_my_info_kb()
        )
        await state.set_state(Form.view_my_info)

    except Exception as e:
        logger.error(f"Ошибка при показе информации: {e}")
        await message.answer("⚠️ Ошибка при загрузке данных")


@router.callback_query(F.data == "show_my_info")
async def handle_show_my_info(callback: CallbackQuery, state: FSMContext):
    await show_complete_user_info(callback.message, state)
    await callback.answer()


@router.message(Command("my_info"))
async def handle_my_info_command(message: Message, state: FSMContext):
    await show_complete_user_info(message, state)