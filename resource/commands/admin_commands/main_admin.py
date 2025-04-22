from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.list_of_interns_kb import list_of_interns_kb
from ...keyboards.list_of_groups_kb import list_of_groups_kb


router = Router()


@router.message(Form.main_admin)
async def main_admin(message: Message, state: FSMContext):
    if message.text == 'Создать задачу':
        await message.answer('Введите название задачи:')
        await state.set_state(Form.create_task_name)
    elif message.text == 'Создать группу':
        await message.answer('Введите название группы:')
        await state.set_state(Form.create_group_name)
    elif message.text == 'Стажеры':
        await message.answer('Список стажеров:',
                             reply_markup=list_of_interns_kb(message.from_user.username))
        await state.set_state(Form.look_interns_info)
    elif message.text == 'Группы':
        await message.answer('Список групп:',
                             reply_markup=list_of_groups_kb(message.from_user.username))
        await state.set_state(Form.look_groups_info)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=admin_keyboard)
