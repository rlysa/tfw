#Посмотреть список задач (отсортированы по дедлайнам)

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from ..forms import Form
from db.db_request.list_tasks import list_tasks
from ...keyboards.list_of_tasks_kb import list_of_tasks_kb

router = Router(name="view_the_task_list_router")  # Добавляем имя роутера


@router.callback_query(Form.view_the_task_list)
async def view_task_list(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    username = user_data.get('username')

    keyboard = list_of_tasks_kb(username)

    if not keyboard:
        await callback.message.edit_text("🎉 У вас пока нет задач!")
    else:
        await callback.message.edit_text(
            "📋 Ваши текущие задачи:",
            reply_markup=keyboard
        )


@router.message(Form.view_the_task_list)
async def handle_task_list_message(message: Message, state: FSMContext):
    if message.text.lower() == 'назад':
        await message.answer("Возвращаемся в главное меню")
        await state.set_state(Form.main_intern)