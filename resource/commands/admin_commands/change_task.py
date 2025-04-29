from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.db_request.list_interns import list_of_interns
from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.back_button import back_kb
from ...keyboards.change_task_kb import change_task_ikb
from ...keyboards.list_of_interns_kb import list_of_interns_select_kb


router = Router()


@router.callback_query(Form.change_delete_task)
async def change_delete_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task = data['task']
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        await callback.message.answer(text=f'Выберите команду:',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    elif callback.data == 'delete':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data='delete')]]))
        await callback.message.answer(text=f'Задача удалена',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    elif callback.data == 'change':
        await callback.message.edit_reply_markup(reply_markup=change_task_ikb)
        await state.set_state(Form.change_task)
        await state.update_data(task=task)


@router.message(Form.change_delete_task)
async def change_delete_task(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


@router.callback_query(Form.change_task)
async def change_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task = data['task']
    if callback.data == 'back':
        await callback.message.delete_reply_markup()
        await callback.message.answer(text=f'Выберите команду:',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
        return
    elif callback.data == 'interns':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить список стажеров', callback_data='name')]]))
        interns = func_list_of_interns(callback.from_user.username)
        await callback.message.answer('Выберите стажеров из списка. Сделав выбор, нажмите "Далее":',
                                      reply_markup=list_of_interns_select_kb(interns, []))
        await state.set_state(Form.change_task_interns)
        await state.update_data(task=task)
        return

    await state.set_state(Form.change_task_new)
    await state.update_data(task=task)
    if callback.data == 'name':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить название', callback_data='name')]]))
        await callback.message.answer('Введите новое название:',
                                      reply_markup=back_kb)
        await state.update_data(type='name')
    elif callback.data == 'deadline':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить дедлайн', callback_data='name')]]))
        await callback.message.answer('Введите новый срок выполнения задачи в формате дд.мм.гггг:',
                                      reply_markup=back_kb)
        await state.update_data(type='deadline')
    elif callback.data == 'description':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить описание', callback_data='name')]]))
        await callback.message.answer('Введите новое описание:',
                                      reply_markup=back_kb)
        await state.update_data(type='description')
    elif callback.data == 'report':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить формат отчета', callback_data='name')]]))
        await callback.message.answer('Введите новый формат отчета:',
                                      reply_markup=back_kb)
        await state.update_data(type='report')


@router.message(Form.change_task)
async def change_task(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


def func_list_of_interns(admin):
    return list_of_interns(admin)


@router.message(Form.change_task_new)
async def change_task_new(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Задача не была изменена:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Ща доработаю, чтоб задачка менялась',
                         reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)


@router.callback_query(Form.change_task_interns)
async def change_task_interns(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer('Некорректный запрос',
                                  reply_markup=admin_keyboard)
    await state.set_state(Form.main_admin)


@router.message(Form.change_task_interns)
async def change_task_interns(message: Message, state: FSMContext):
    await message.answer('Ща доработаю, чтоб задачка менялась',
                         reply_markup=admin_keyboard)
    await state.set_state(Form.main_admin)
