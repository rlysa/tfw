from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from db.db_request.list_admins import list_of_admins, admins_info, new_keys
from resource.commands.forms import Form
from resource.keyboards.admin_father_keyboard import admin_father_keyboard
from db.db_request.list_interns import list_of_interns, interns_info
from db.db_request.delete_user import delete_user
from resource.keyboards.change_task_group_profile_kb import delete_intern_ikb


router = Router()


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
        func_delete_user(username, 3)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data='delete')]]))
        await callback.message.answer(text=f'Стажер удален',
                                      reply_markup=admin_father_keyboard)
        await state.set_state(Form.main_admin_father)


@router.message(Form.delete_intern_af)
async def delete_intern_af(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


def func_delete_user(username, role):
    delete_user(username, role)


@router.callback_query(Form.look_admins_af)
async def look_admins_af(callback: CallbackQuery, state: FSMContext):
    list_admins = '\n'.join([i[0] for i in list_of_admins()])
    if callback.data == 'back':
        await callback.message.delete()
        await callback.message.answer(text=f'Список админов:\n\n{list_admins}',
                                      reply_markup=admin_father_keyboard)
        await state.set_state(Form.main_admin_father)
    elif callback.data == 'new_keys':
        await callback.message.delete()
        await callback.message.answer(text=f'Список админов:\n\n{list_admins}')
        new_keys()
        await callback.message.answer(text=f'Ключи обновлены',
                                      reply_markup=admin_father_keyboard)
        await state.set_state(Form.main_admin_father)
    else:
        username = callback.data
        info = admins_info(username)
        await callback.message.edit_text(text=f'Список админов:\n\n{list_admins}')
        await callback.message.answer(
            text=f'{info[0]}\n@{username}\nКлюч: {info[1]}',
            reply_markup=delete_intern_ikb)
        await state.set_state(Form.delete_admin_af)
        await state.update_data(username=username)


@router.message(Form.look_admins_af)
async def look_admins_af(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


@router.callback_query(Form.delete_admin_af)
async def delete_admin_af(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        await callback.message.answer(text=f'Выберите команду:',
                                      reply_markup=admin_father_keyboard)
        await state.set_state(Form.main_admin_father)
    elif callback.data == 'delete':
        data = await state.get_data()
        username = data['username']
        func_delete_user(username, 2)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data='delete')]]))
        await callback.message.answer(text=f'Админ удален',
                                      reply_markup=admin_father_keyboard)
        await state.set_state(Form.main_admin_father)


@router.message(Form.delete_admin_af)
async def delete_admin_af(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')
