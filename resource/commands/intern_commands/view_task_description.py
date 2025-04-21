import aiogram
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from db.db_request.task_description import get_task_description, change_task_status
from ...keyboards.task_description_kb import get_task_description_kb
from ...keyboards.list_of_tasks_kb import list_of_tasks_kb
import logging


router = aiogram.Router(name="view_task_description_router")
logger = logging.getLogger(__name__)


async def show_task_description(message: Message, task_id: int):
    """
    Отображает описание задачи с кнопками управления

    Args:
        message: Объект сообщения
        task_id: ID задачи
    """
    task_info = get_task_description(task_id)
    if not task_info:
        await message.answer("⚠️ Задача не найдена")
        return False

    name, description, deadline, status = task_info
    is_done = status == "✅ Завершена"

    message_text = (
        f"📌 {name}\n\n"
        f"📝 Описание:\n{description}\n\n"
        f"⏳ Срок выполнения: {deadline}\n"
        f"🔄 Статус: {status}"
    )

    await message.edit_text(
        text=message_text,
        reply_markup=get_task_description_kb(task_id, is_done)
    )
    return True


@router.callback_query(aiogram.F.data.startswith("view_task_"))
async def handle_view_task(callback: CallbackQuery, state: FSMContext):
    """Обработчик просмотра задачи"""
    task_id = int(callback.data.split("_")[2])
    await show_task_description(callback.message, task_id)
    await callback.answer()


@router.callback_query(aiogram.F.data.startswith("change_status_"))
async def handle_change_status(callback: CallbackQuery, state: FSMContext):
    """Обработчик изменения статуса задачи"""
    task_id = int(callback.data.split("_")[2])

    if change_task_status(task_id):
        await show_task_description(callback.message, task_id)
        await callback.answer("Статус задачи обновлен!")
    else:
        await callback.answer("⚠️ Не удалось изменить статус")


@router.callback_query(aiogram.F.data == "back_to_tasks_list")
async def handle_back_to_list(callback: CallbackQuery, state: FSMContext):
    """Обработчик возврата к списку задач"""
    username = callback.from_user.username
    keyboard = list_of_tasks_kb(username)

    if not keyboard or not keyboard.inline_keyboard:
        await callback.message.edit_text("🎉 У вас пока нет активных задач")
    else:
        await callback.message.edit_text(
            "📋 Список ваших задач:",
            reply_markup=keyboard
        )
    await callback.answer()