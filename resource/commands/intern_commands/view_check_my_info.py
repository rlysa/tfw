from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.db_request.check_my_info import get_user_info
from resource.keyboards.check_my_info_kb import get_my_info_kb
from resource.commands.forms import Form
import logging

router = Router(name="view_check_my_info_router")
logger = logging.getLogger(__name__)

def format_user_info(user_data: dict) -> str:
    role_map = {
        1: "👑 Главный администратор",
        2: "👨‍💼 Администратор",
        3: "👨‍🎓 Стажёр"
    }
    return (
        f"👤 <b>Ваша информация:</b>\n\n"
        f"📛 <b>ФИО:</b> {user_data['surname']} {user_data['name']} {user_data['middle_name']}\n"
        f"🔹 <b>Логин:</b> @{user_data['username']}\n"
        f"👔 <b>Роль:</b> {role_map.get(user_data['role'], 'Неизвестно')}"
    )

async def show_user_info(message: Message, state: FSMContext):
    try:
        # Получаем username из сообщения пользователя
        username = message.from_user.username
        if not username:
            await message.answer("❌ У вас не установлен username в Telegram. Пожалуйста, установите его в настройках.")
            return

        # Добавляем логирование для отладки
        logger.info(f"Запрос информации для пользователя: @{username}")

        user_data = get_user_info(username)
        if not user_data:
            await message.answer("ℹ️ Ваш профиль не найден в системе. Обратитесь к администратору.")
            await message.answer(username)
            return

        await message.answer(
            text=format_user_info(user_data),
            reply_markup=get_my_info_kb()
        )
        await state.set_state(Form.view_my_info)

    except Exception as e:
        logger.error(f"Ошибка при показе информации: {e}")
        await message.answer("⚠️ Произошла ошибка при загрузке ваших данных")

@router.callback_query(F.data == "show_my_info")
async def handle_show_my_info(callback: CallbackQuery, state: FSMContext):
    await show_user_info(callback.message, state)
    await callback.answer()

@router.message(Command("my_info"))
async def handle_my_info_command(message: Message, state: FSMContext):
    await show_user_info(message, state)