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
    """Форматирует информацию о группе в читаемый текст"""
    message = [
        f"👥 Группа: {group_data['group_name']}",
        f"👨‍💼 Руководитель: {group_data['admin_info']['full_name']} (@{group_data['admin_info']['username']})\n",
        "📌 Стажёры в группе:"
    ]

    # Добавляем информацию о каждом стажёре
    interns = group_data.get('interns_info', [])
    for i, intern in enumerate(interns, 1):
        message.append(f"{i}. {intern['full_name']} (@{intern['username']})")

    if not interns:
        message.append("Других стажёров в группе нет")

    return "\n".join(message)


async def process_group_request(source: CallbackQuery | Message, state: FSMContext):
    """Обрабатывает запрос на просмотр группы"""
    try:
        user = source.from_user
        username = user.username

        if not username:
            error_msg = "❌ Для просмотра группы нужно установить username в настройках Telegram"
            if isinstance(source, CallbackQuery):
                await source.answer(error_msg, show_alert=True)
            else:
                await source.answer(error_msg)
            return

        logger.debug(f"Запрос группы от @{username} (ID: {user.id})")

        group_data = get_group_composition(username)

        if not group_data:
            debug_msg = (
                f"ℹ️ Вы не состоите ни в одной группе\n\n"
                f"Username: @{username}\n"
                f"User ID: {user.id}"
            )
            if isinstance(source, CallbackQuery):
                await source.message.edit_text(debug_msg)
            else:
                await source.answer(debug_msg)
            return

        response = format_group_message(group_data)

        if isinstance(source, CallbackQuery):
            await source.message.edit_text(
                text=response,
                reply_markup=get_group_composition_kb()
            )
        else:
            await source.answer(
                text=response,
                reply_markup=get_group_composition_kb()
            )

        await state.set_state(Form.view_group_composition)

    except Exception as e:
        error_msg = (
            f"⚠️ Произошла ошибка при загрузке группы\n\n"
            f"Username: @{getattr(user, 'username', 'не определен')}\n"
            f"Ошибка: {str(e)}"
        )
        logger.error(f"Ошибка при обработке запроса группы: {str(e)}")
        if isinstance(source, CallbackQuery):
            await source.answer(error_msg, show_alert=True)
        else:
            await source.answer(error_msg)
    finally:
        if isinstance(source, CallbackQuery):
            await source.answer()


@router.callback_query(F.data == "show_my_group")
async def show_group_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик нажатия кнопки 'Моя группа'"""
    await process_group_request(callback, state)


@router.message(Command("my_group"))
async def group_command_handler(message: Message, state: FSMContext):
    """Обработчик команды /my_group"""
    await process_group_request(message, state)