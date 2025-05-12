from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard, tasks_keyboard, group_keyboard, interns_keyboard
from ...keyboards.list_of_interns_kb import list_of_interns_kb
from ...keyboards.list_of_groups_kb import list_of_groups_kb
from ...keyboards.list_of_tasks_kb import list_of_tasks_admin_kb
from ...keyboards.back_button import back_kb
from ...keyboards.change_task_group_profile_kb import change_profile_ikb
from db.db_request.admins_profile import profile_info


router = Router()


@router.message(Form.main_admin_father)
async def main_admin_father(message: Message, state: FSMContext):
    if message.text == 'Стажеры':
        await message.answer('Выберите команду:',
                             reply_markup=interns_keyboard)
        await state.set_state(Form.interns_commands)
    elif message.text == 'Администраторы':
        await message.answer('Выберите команду:',
                             reply_markup=interns_keyboard)
        await state.set_state(Form.interns_commands)
    elif message.text == 'Профиль':
        profile = profile_info(message.from_user.username)
        await message.answer(f'ФИО: {profile[1]}\nКлюч: {profile[0]}',  # поменять, в разделе профиль добавить кнопку "получить ключ", которая обновляет ключ для регистрации стажера
                             reply_markup=change_profile_ikb)
        await state.set_state(Form.look_profile)
        await state.update_data(role=1)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=admin_keyboard)


@router.message(Form.interns_commands)
async def interns_commands(message: Message, state: FSMContext):
    if message.text == 'Посмотреть список':
        await message.answer('Список стажеров:',
                             reply_markup=list_of_interns_kb(message.from_user.username))
        await state.set_state(Form.look_interns_info)
    elif message.text == 'Поиск по скиллам':
        # await message.answer('В разработке',
        #                      reply_markup=admin_keyboard)
        await message.answer('Введите слово для поиска:',
                             reply_markup=back_kb)
        await state.set_state(Form.skill_search)
    elif message.text == 'Отправить сообщение стажеру':
        await message.answer('Введите текст сообщения:',
                             reply_markup=back_kb)
        await state.set_state(Form.send_message_text)
    elif message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=tasks_keyboard)
