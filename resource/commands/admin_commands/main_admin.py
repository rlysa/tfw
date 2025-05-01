from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard, tasks_keyboard, group_keyboard
from ...keyboards.list_of_interns_kb import list_of_interns_kb
from ...keyboards.list_of_groups_kb import list_of_groups_kb
from ...keyboards.list_of_tasks_kb import list_of_tasks_admin_kb
from ...keyboards.back_button import back_kb
from ...keyboards.change_profile_kb import change_profile_keyboard
from db.db_request.admins_profile import profile


router = Router()


@router.message(Form.main_admin)
async def main_admin(message: Message, state: FSMContext):
    if message.text == 'Задачи':
        await message.answer('Выберите команду:',
                             reply_markup=tasks_keyboard)
        await state.set_state(Form.tasks_command)
    elif message.text == 'Группы':
        await message.answer('Выберите команду:',
                             reply_markup=group_keyboard)
        await state.set_state(Form.groups_commands)
    elif message.text == 'Стажеры':
        await message.answer('Список стажеров:',
                             reply_markup=list_of_interns_kb(message.from_user.username))
        await state.set_state(Form.look_interns_info)
    elif message.text == 'Профиль':
        pr = profile(message.from_user.username)
        await message.answer(f'ФИО: {pr[1]}\nКлюч: {pr[0]}',  # поменять, в разделе профиль добавить кнопку "получить ключ", которая обновляет ключ для регистрации стажера
                             reply_markup=change_profile_keyboard)
        await state.set_state(Form.look_profile)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=admin_keyboard)


@router.message(Form.tasks_command)
async def tasks_commands(message: Message, state: FSMContext):
    if message.text == 'Создать задачу':
        await message.answer('Введите название задачи:',
                             reply_markup=back_kb)
        await state.set_state(Form.create_task_name)
    elif message.text == 'Посмотреть задачи':
        await message.answer('Список задач:',
                             reply_markup=list_of_tasks_admin_kb(message.from_user.username))
        await state.set_state(Form.look_tasks)
    # elif message.text == 'Изменить задачу':
    #     await message.answer('В разработке',
    #                          reply_markup=tasks_keyboard)
    # elif message.text == 'Удалить задачу':
    #     await message.answer('В разработке',
    #                          reply_markup=tasks_keyboard)
    elif message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=tasks_keyboard)


@router.message(Form.groups_commands)
async def groups_commands(message: Message, state: FSMContext):
    if message.text == 'Создать группу':
        await message.answer('Введите название группы:',
                             reply_markup=back_kb)
        await state.set_state(Form.create_group_name)
    elif message.text == 'Посмотреть группы':
        await message.answer('Список групп:',
                             reply_markup=list_of_groups_kb(message.from_user.username))
        await state.set_state(Form.look_groups_info)
    # elif message.text == 'Изменить группу':
    #     await message.answer('В разработке',
    #                          reply_markup=group_keyboard)
    # elif message.text == 'Удалить группу':
    #     await message.answer('В разработке',
    #                          reply_markup=group_keyboard)
    elif message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=group_keyboard)
