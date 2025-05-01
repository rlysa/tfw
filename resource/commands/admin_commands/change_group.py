from pstats import func_get_function_name

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.db_request.list_groups import groups_info
from db.db_request.list_interns import list_of_interns
from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.back_button import back_kb
from ...keyboards.change_task_group_profile_kb import change_group_ikb
from ...keyboards.list_of_interns_kb import list_of_interns_select_kb, list_of_interns_selected_kb
from db.db_request.delete_group import delete_group
from db.db_request.change_group import change_groups_info


router = Router()


@router.callback_query(Form.change_delete_group)
async def change_delete_group(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    group = data['group']
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        await callback.message.answer(text=f'Выберите команду:',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    elif callback.data == 'delete':
        func_delete_group(group)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data='delete')]]))
        await callback.message.answer(text=f'Группа удалена',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    elif callback.data == 'change':
        await callback.message.edit_reply_markup(reply_markup=change_group_ikb)
        await state.set_state(Form.change_group)
        await state.update_data(group=group)


@router.message(Form.change_delete_group)
async def change_delete_group(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


def func_delete_group(groups_id):
    delete_group(groups_id)


@router.callback_query(Form.change_group)
async def change_group(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    group = data['group']
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        await callback.message.answer(text=f'Выберите команду:',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    elif callback.data == 'name':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить название', callback_data='name')]]))
        await callback.message.answer('Введите новое название:',
                                      reply_markup=back_kb)
        await state.set_state(Form.change_group_name)
    elif callback.data == 'interns':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить список стажеров', callback_data='name')]]))
        interns = func_list_of_interns(callback.from_user.username)
        await state.update_data(interns=interns)
        await callback.message.answer('Выберите стажеров из списка. Сделав выбор, нажмите "Далее"',
                                      reply_markup=list_of_interns_select_kb(interns, []))
        await state.update_data(selected=[])
        await state.set_state(Form.change_group_interns)
    await state.update_data(group=group)


@router.message(Form.change_group)
async def change_group(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


def func_list_of_interns(admin):
    return list_of_interns(admin)


@router.message(Form.change_group_name)
async def change_group_name(message: Message, state: FSMContext):
    data = await state.get_data()
    group = data['group']
    text = message.text
    if text == 'Меню команд':
        await message.answer('Группа не была изменена',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
        return

    if len(text) > 30:
        await message.answer('Макс. количество символов: 30\nВведите название группы:',
                             reply_markup=back_kb)
        return

    if func_change_group(group, 'name', text):
        info = groups_info(group)
        info[1] = "\n".join(info[1])
        await message.answer('Группа изменена')
        await message.answer(text=f'{info[0]}\n\n{info[1]}',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)


@router.callback_query(Form.change_group_interns)
async def change_group_interns(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_interns = data['selected']
    group = data['group']
    if callback.data == 'next':
        await callback.message.edit_reply_markup(
            reply_markup=list_of_interns_selected_kb(data['interns'], selected_interns)
        )
        if func_change_group(group, 'interns', ' '.join(selected_interns)):
            info = groups_info(group)
            info[1] = "\n".join(info[1])
            await callback.message.answer('Группа изменена')
            await callback.message.answer(text=f'{info[0]}\n\n{info[1]}',
                                 reply_markup=admin_keyboard)
            await state.set_state(Form.main_admin)
    elif callback.data == 'back':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Меню команд', callback_data='back')]]))
        await callback.message.answer(text=f'Группа не была изменена',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        if callback.data in selected_interns:
            selected_interns.pop(selected_interns.index(callback.data))
        else:
            selected_interns.append(callback.data)
        await state.update_data(selected=selected_interns)
        await callback.message.edit_reply_markup(
            reply_markup=list_of_interns_select_kb(data['interns'], selected_interns))


@router.message(Form.change_group_interns)
async def change_group_interns(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос',
                         reply_markup=back_kb)


def func_change_group(groups_id, field, value):
    if change_groups_info(groups_id, field, value):
        return True
    return False
