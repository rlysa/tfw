#Посмотреть список задач (отсортированы по дедлайнам)

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from ..forms import Form
from db.db_request.list_tasks import list_tasks
from ...keyboards.list_of_tasks_kb import list_of_tasks_kb

router = Router(name="view_the_task_list_router")


@router.callback_query(Form.view_the_task_list)
async def view_task_list(callback: CallbackQuery, state: FSMContext):
    # Обработка callback для состояния view_the_task_list
    username = callback.from_user.username
    keyboard = list_of_tasks_kb(username)

    if not keyboard:
        await callback.message.answer("🎉 Поздравляем! У вас пока нет активных задач.")
    else:
        await callback.message.answer(
            "📋 Список ваших текущих задач (отсортирован по срокам выполнения):",
            reply_markup=keyboard
        )


# Отдельный обработчик для кнопки "show_my_tasks"
@router.callback_query(lambda callback: callback.data == "show_my_tasks")
async def handle_show_my_tasks(callback: CallbackQuery, state: FSMContext):
    username = callback.from_user.username
    keyboard = list_of_tasks_kb(username)

    if not keyboard:
        await callback.message.answer("🎉 Поздравляем! У вас пока нет активных задач.")
    else:
        await callback.message.answer(
            "📋 Список ваших текущих задач (отсортирован по срокам выполнения):",
            reply_markup=keyboard
        )

    await state.set_state(Form.view_the_task_list)


@router.message(Form.view_the_task_list)
async def handle_task_list_message(message: Message, state: FSMContext):
    if message.text and message.text.lower() == 'назад':
        await message.answer("🔙 Возвращаемся в главное меню")
        await state.set_state(Form.main_intern)
    else:
        await message.answer("Пожалуйста, используйте кнопки для навигации")