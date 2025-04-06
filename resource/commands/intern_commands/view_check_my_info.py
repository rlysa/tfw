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
        "👤 ПОЛНАЯ ИНФОРМАЦИЯ",
        "",
        f"📛 ФИО: {user_data.get('surname', '')} {user_data.get('name', '')} {user_data.get('middle_name', '')}",
        f"🔹 Логин: @{user_data.get('username', '')}",
        f"👔 Роль: {role_map.get(user_data.get('role'), 'Неизвестно')}",
    ]

    # Навыки
    if user_data.get('skills'):
        message.append(f"🛠 Навыки: {user_data['skills']}")

    return "\n".join(message)


async def show_user_info(target: Message | CallbackQuery, state: FSMContext):
    """Общая функция для отображения информации (для сообщений и callback)"""
    try:
        # Получаем user из правильного источника
        user = target.from_user if isinstance(target, Message) else target.from_user

        if not user.username:
            await (target.answer if isinstance(target, Message) else target.answer)(
                "❌ У вас не установлен username в Telegram",
                show_alert=isinstance(target, CallbackQuery)
            )
            return

        logger.debug(f"Запрос информации для пользователя: {user.username} (ID: {user.id})")

        user_data = get_full_user_info(user.username)
        if not user_data:
            response = "ℹ️ Ваш профиль не найден в системе"
            await (target.answer if isinstance(target, Message) else target.message.edit_text)(response)
            return

        response_text = format_complete_user_info(user_data)

        if isinstance(target, Message):
            await target.answer(response_text, reply_markup=get_my_info_kb())
        else:
            await target.message.edit_text(response_text, reply_markup=get_my_info_kb())

        await state.set_state(Form.view_my_info)

    except Exception as e:
        logger.error(f"Ошибка при показе информации: {e}")
        error_msg = "⚠️ Ошибка при загрузке данных"
        await (target.answer if isinstance(target, Message) else target.answer)(error_msg, show_alert=True)


@router.callback_query(F.data == "show_my_info")
async def handle_show_my_info(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Моя информация'"""
    await show_user_info(callback, state)
    await callback.answer()


@router.message(Command("my_info"))
async def handle_my_info_command(message: Message, state: FSMContext):
    """Обработчик команды /my_info"""
    await show_user_info(message, state)