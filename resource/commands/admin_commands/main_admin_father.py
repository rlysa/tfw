from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import interns_keyboard
from ...keyboards.admin_father_keyboard import admin_father_keyboard
from ...keyboards.list_of_interns_kb import list_of_interns_kb
from ...keyboards.change_task_group_profile_kb import change_profile_ikb
from db.db_request.admins_profile import profile_info
from db.db_request.list_interns import list_of_interns, interns_info
from db.db_request.delete_user import delete_user
from ...keyboards.change_task_group_profile_kb import delete_intern_ikb


router = Router()


@router.message(Form.main_admin_father)
async def main_admin_father(message: Message, state: FSMContext):
    if message.text == 'Стажеры':
        await message.answer('Список стажеров:',
                             reply_markup=list_of_interns_kb('all'))
        await state.set_state(Form.look_interns_af)
    elif message.text == 'Администраторы':
        await message.answer('Выберите команду:',
                             reply_markup=interns_keyboard)
        await state.set_state(Form.interns_commands)
    elif message.text == 'Профиль':
        profile = profile_info(message.from_user.username)
        await message.answer(f'ФИО: {profile[1]}',  # поменять, в разделе профиль добавить кнопку "получить ключ", которая обновляет ключ для регистрации стажера
                             reply_markup=change_profile_ikb)
        await state.set_state(Form.look_profile)
        await state.update_data(role=1)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=admin_father_keyboard)


@router.callback_query(Form.look_interns_af)
async def look_interns_af(callback: CallbackQuery, state: FSMContext):
    list_interns = '\n'.join([i[0] for i in list_of_interns('all')])
    if callback.data == 'back':
        await callback.message.delete()
        await callback.message.answer(text=f'Список стажеров:\n\n{list_interns}',
                                      reply_markup=admin_father_keyboard)
        await state.set_state(Form.main_admin_father)
    else:
        username = callback.data
        info = interns_info(username)
        await callback.message.edit_text(text=f'Список стажеров:\n\n{list_interns}')
        await callback.message.answer(
            text=f'{info[0]}\n@{username}',
            reply_markup=delete_intern_ikb)
        await state.set_state(Form.delete_intern_af)
        await state.update_data(username=username)


@router.message(Form.look_interns_af)
async def look_interns_af(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


@router.callback_query(Form.delete_intern_af)
async def delete_intern_af(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        await callback.message.answer(text=f'Выберите команду:',
                                      reply_markup=admin_father_keyboard)
        await state.set_state(Form.main_admin_father)
    elif callback.data == 'delete':
        data = await state.get_data()
        username = data['username']
        func_delete_intern(username)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data='delete')]]))
        await callback.message.answer(text=f'Стажер удален',
                                      reply_markup=admin_father_keyboard)
        await state.set_state(Form.main_admin_father)


@router.message(Form.delete_intern_af)
async def delete_intern_af(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


def func_delete_intern(username):
    delete_user(username, 3)
