import json

from aiogram import Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from ..forms import Form
from db.db_request.list_interns import list_of_interns, interns_info, interns_resume
from db.db_request.delete_user import delete_user
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.back_button import back_kb
from ...keyboards.change_task_group_profile_kb import delete_intern_ikb


router = Router()


@router.callback_query(Form.look_interns_info)
async def look_interns_info(callback: CallbackQuery, state: FSMContext):
    list_interns = '\n'.join([i[0] for i in list_of_interns(callback.from_user.username)])
    if callback.data == 'back':
        await callback.message.delete()
        await callback.message.answer(text=f'Список стажеров:\n\n{list_interns}',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        username = callback.data
        info = interns_info(username)
        await callback.message.edit_text(text=f'Список стажеров:\n\n{list_interns}')
        await callback.message.answer(
            text=f'{info[0]}\n@{username}\n\nСкиллы:\n{info[1]}\n\nГруппы:\n{info[2]}\n\nЗадачи:\n{info[3]}',
            reply_markup=delete_intern_ikb)
        await state.set_state(Form.delete_intern)
        await state.update_data(username=username)


@router.message(Form.look_interns_info)
async def look_interns_info(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


@router.callback_query(Form.delete_intern)
async def delete_intern(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        await callback.message.answer(text=f'Выберите команду:',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    elif callback.data == 'delete':
        data = await state.get_data()
        username = data['username']
        func_delete_intern(username)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data='delete')]]))
        await callback.message.answer(text=f'Стажер удален',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    elif callback.data == 'resume':
        data = await state.get_data()
        username = data['username']
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Резюме', callback_data='resume')]]))
        report = json.loads(interns_resume(username))
        if report.get('file_type') == 'document':
            await callback.message.answer_document(report.get('file_id'),
                                                   reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)


@router.message(Form.delete_intern)
async def delete_intern(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


def func_delete_intern(username):
    delete_user(username, 3)
