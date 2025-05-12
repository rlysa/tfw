from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from resource.commands.forms import Form
from resource.keyboards.admin_keyboard import interns_keyboard
from resource.keyboards.admin_father_keyboard import admin_father_keyboard
from resource.keyboards.list_of_interns_kb import list_of_interns_kb, list_of_admins_kb
from resource.keyboards.change_task_group_profile_kb import change_profile_ikb
from db.db_request.admins_profile import profile_info


router = Router()


@router.message(Form.main_admin_father)
async def main_admin_father(message: Message, state: FSMContext):
    if message.text == 'Стажеры':
        await message.answer('Список стажеров:',
                             reply_markup=list_of_interns_kb('all'))
        await state.set_state(Form.look_interns_af)
    elif message.text == 'Администраторы':
        await message.answer('Список админов:',
                             reply_markup=list_of_admins_kb())
        await state.set_state(Form.look_admins_af)
    elif message.text == 'Профиль':
        profile = profile_info(message.from_user.username)
        await message.answer(f'ФИО: {profile[1]}',  # поменять, в разделе профиль добавить кнопку "получить ключ", которая обновляет ключ для регистрации стажера
                             reply_markup=change_profile_ikb)
        await state.set_state(Form.look_profile)
        await state.update_data(role=1)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=admin_father_keyboard)
