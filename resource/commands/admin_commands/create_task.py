from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from db.db_request.create_task import new_task


router = Router()


@router.message(Form.create_task_name)
async def create_task_get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Выберите стажеров: (здесь будет список)')
    await state.set_state(Form.create_task_interns)


@router.message(Form.create_task_interns)  # заменить на callback_query
async def create_task_get_interns(message: Message, state: FSMContext):
    await state.update_data(interns='user1')
    await message.answer('Введите описание задачи:')
    await state.set_state(Form.create_task_description)


@router.message(Form.create_task_description)
async def create_task_get_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Укажите сроки выполнения задачи в формате дд.мм.гггг:')
    await state.set_state(Form.create_task_deadline)


@router.message(Form.create_task_deadline)
async def create_task_get_deadline(message: Message, state: FSMContext):
    await state.update_data(deadline=message.text)  # сделать проверку на ввод: правильный формат, дата не раньше сегодняшней
    await message.answer('Укажите формат отчета о выполнении задач (мб тоже список)')
    await state.set_state(Form.create_task_report)


@router.message(Form.create_task_report)
async def create_task_get_report(message: Message, state: FSMContext):
    await state.update_data(report=message.text)
    data = await state.get_data()
    create_task(data, message.from_user.username)
    await message.answer('Задача создана', reply_markup=admin_keyboard)
    await state.set_state(Form.main_admin)


def create_task(task, admin):
    new_task(task, admin)
