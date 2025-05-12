from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.admin_father_keyboard import admin_father_keyboard
from ...keyboards.back_button import back_kb
from ...keyboards.change_task_group_profile_kb import what_change_profile_ikb
from db.db_request.admins_profile import change_profile_info, profile_info


router = Router()


@router.callback_query(Form.look_profile)
async def look_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    role = 1 if 'role' in data else 2
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        keyboard = admin_keyboard if role == 2 else admin_father_keyboard
        st = Form.main_admin if role == 2 else Form.main_admin_father
        await callback.message.answer(text=f'Выберите команду:',
                                      reply_markup=keyboard)
        await state.set_state(st)
    elif callback.data == 'change':
        await callback.message.edit_reply_markup(reply_markup=what_change_profile_ikb)
        await state.set_state(Form.change_profile)
        await state.update_data(role=role)


@router.message(Form.look_profile)
async def look_profile(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


@router.callback_query(Form.change_profile)
async def change_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    role = data['role']
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        keyboard = admin_keyboard if role == 2 else admin_father_keyboard
        st = Form.main_admin if role == 2 else Form.main_admin_father
        await callback.message.answer(text=f'Профиль не был изменен',
                                      reply_markup=keyboard)
        await state.set_state(st)
        return
    elif callback.data == 'surname':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить фамилию', callback_data='surname')]]))
        await callback.message.answer('Введите фамилию:',
                                      reply_markup=back_kb)
        await state.update_data(field='surname')
    elif callback.data == 'name':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить имя', callback_data='name')]]))
        await callback.message.answer('Введите имя:',
                                      reply_markup=back_kb)
        await state.update_data(field='name')
    elif callback.data == 'middle_name':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить отчество', callback_data='middle_name')]]))
        await callback.message.answer('Введите отчество:',
                                      reply_markup=back_kb)
        await state.update_data(field='middle_name')
    await state.set_state(Form.change_profile_new)
    await state.update_data(role=role)


@router.message(Form.change_profile)
async def change_profile(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


@router.message(Form.change_profile_new)
async def change_profile_new(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data['field']
    role = data['role']
    text = message.text
    keyboard = admin_keyboard if role == 2 else admin_father_keyboard
    st = Form.main_admin if role == 2 else Form.main_admin_father
    if text == 'Меню команд':
        await message.answer('Профиль не был изменен',
                             reply_markup=keyboard)
        await state.set_state(st)
        return

    if len(text) > 30:
        await message.answer('Макс. количество символов: 30\nВведите еще раз:',
                             reply_markup=back_kb)
        return

    if func_change_profile(message.from_user.username, field, text):
        profile = profile_info(message.from_user.username)
        await message.answer('Профиль изменен')
        await message.answer(f'ФИО: {profile[1]}\nКлюч: {profile[0]}',
                             reply_markup=keyboard)
        await state.set_state(st)


def func_change_profile(username, field, value):
    if change_profile_info(username, field, value):
        return True
    return False
