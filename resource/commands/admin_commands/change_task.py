from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from datetime import datetime

from config import TOKEN
from db.db_request.list_interns import list_of_interns, interns_ids
from db.db_request.list_tasks import tasks_info_admin
from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.back_button import back_kb
from ...keyboards.change_task_group_profile_kb import change_task_ikb, report_format_ikb
from ...keyboards.list_of_interns_kb import list_of_interns_select_kb, list_of_interns_selected_kb
from db.db_request.change_task import change_tasks_info
from db.db_request.delete_task import delete_task
from db.db_request.list_tasks import tasks_info_admin


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
        func_delete_task(task)
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
    elif callback.data == 'return':
        if func_change_task(task, 'done', 'False'):
            await callback.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text='Вернуть на доработку', callback_data='return')]]))
            await callback.message.answer(text=f'Задача отправлена на доработку',
                                          reply_markup=admin_keyboard)
            info = tasks_info_admin(task)
            ids = interns_ids(info[2].split())
            bot = Bot(TOKEN)
            for i in ids:
                await bot.send_message(chat_id=i,
                                       text=f'Задача "{info[1]}" возвращена на доработку')
            await bot.session.close()
            await state.set_state(Form.main_admin)
    elif callback.data == 'report':
        info = tasks_info_admin(task)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Посмотреть отчет', callback_data='report')]]))
        if info[-2] == 'Файл':
            # file = InputFile('Отчет 1.pdf')
            # await callback.message.answer_document(file)
            await callback.message.answer(text=f'Файл',
                                          reply_markup=admin_keyboard)
        else:
            await callback.message.answer(text=f'Отчет:\n{info[-1]}',
                                          reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)


@router.message(Form.change_delete_task)
async def change_delete_task(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


def func_delete_task(tasks_id):
    delete_task(tasks_id)


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
                inline_keyboard=[[InlineKeyboardButton(text='Изменить список стажеров', callback_data='interns')]]))
        interns = func_list_of_interns(callback.from_user.username)
        await state.update_data(interns=interns)
        await callback.message.answer('Выберите стажеров из списка. Сделав выбор, нажмите "Далее"',
                                      reply_markup=list_of_interns_select_kb(interns, []))
        await state.update_data(selected=[])
        await state.set_state(Form.change_task_interns)
        await state.update_data(task=task)
        return
    elif callback.data == 'report':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить формат отчета', callback_data='report')]]))
        await callback.message.answer('Укажите новый формат отчета:',
                                      reply_markup=report_format_ikb)
        await state.set_state(Form.change_task_report)
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
        await state.update_data(field='name')
    elif callback.data == 'deadline':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить дедлайн', callback_data='deadline')]]))
        await callback.message.answer('Введите новый срок выполнения задачи в формате дд.мм.гггг:',
                                      reply_markup=back_kb)
        await state.update_data(field='deadline')
    elif callback.data == 'description':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить описание', callback_data='description')]]))
        await callback.message.answer('Введите новое описание:',
                                      reply_markup=back_kb)
        await state.update_data(field='description')


@router.message(Form.change_task)
async def change_task(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


def func_list_of_interns(admin):
    return list_of_interns(admin)


@router.message(Form.change_task_new)
async def change_task_new(message: Message, state: FSMContext):
    data = await state.get_data()
    task, field = data['task'], data['field']
    text = message.text
    if text == 'Меню команд':
        await message.answer('Задача не была изменена',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
        return

    if field == 'name' and len(text) > 30:
        await message.answer('Макс. количество символов: 30\nВведите название задачи:',
                             reply_markup=back_kb)
        return
    elif field == 'deadline':
        try:
            if (datetime.strptime(text, "%d.%m.%Y").date() - datetime.today().date()).days < 1:
                await message.answer(
                    'Срок выполнения может быть назначен не ранее чем на завтра. Укажите сроки выполнения задачи в формате дд.мм.гггг:',
                    reply_markup=back_kb)
                return
            else:
                text = datetime.strptime(text, "%d.%m.%Y").date()
        except Exception as e:
            await message.answer('Дата указана неверно. Укажите сроки выполнения задачи в формате дд.мм.гггг:',
                                 reply_markup=back_kb)
            return
    elif field == 'description' and len(text) > 3000:
        await message.answer('Макс. количество символов: 3000\nВведите описание задачи:',
                             reply_markup=back_kb)
        return

    if func_change_task(task, field, text):
        info = tasks_info_admin(task)
        interns = '\n'.join(
            [' - @'.join(i) for i in list_of_interns(message.from_user.username) if i[1] in info[2].split()])
        await message.answer('Задача изменена')
        await message.answer(
            text=f'Название: {info[1]}\n\nСтажеры:\n{interns}\nДедлайн: {'.'.join(info[5].split('-')[::-1])}\nОписание: {
            info[4]}\nФормат отчета: {info[6]}\nСтатус: {"не выполнена" if info[-1] != False else "выполнена"}',
            reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)


@router.callback_query(Form.change_task_report)
async def change_task_report(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'back':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Меню команд', callback_data='back')]]))
        await callback.message.answer(text=f'Задача не была изменена',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)

    if callback.data == 'no_report':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Без отчета', callback_data='no_report')]]
            )
        )
    elif callback.data == 'message':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Сообщение', callback_data='message')]]
            )
        )
    elif callback.data == 'file':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Файл', callback_data='file')]]
            )
        )

    data = await state.get_data()
    task = data['task']

    if func_change_task(task, 'report', callback.data):
        info = tasks_info_admin(task)
        interns = '\n'.join(
            [' - @'.join(i) for i in list_of_interns(callback.from_user.username) if i[1] in info[2].split()])
        await callback.message.answer('Задача изменена')
        await callback.message.answer(
            text=f'Название: {info[1]}\n\nСтажеры:\n{interns}\nДедлайн: {'.'.join(info[5].split('-')[::-1])}\nОписание: {
            info[4]}\nФормат отчета: {info[6]}\nСтатус: {"не выполнена" if info[-1] != False else "выполнена"}',
            reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)


@router.message(Form.change_task_report)
async def change_task_report(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


@router.callback_query(Form.change_task_interns)
async def change_task_interns(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_interns = data['selected']
    task = data['task']
    if callback.data == 'next':
        await callback.message.edit_reply_markup(
            reply_markup=list_of_interns_selected_kb(data['interns'], selected_interns)
        )
        if func_change_task(task, 'interns', ' '.join(selected_interns)):
            info = tasks_info_admin(task)
            interns = '\n'.join(
                [' - @'.join(i) for i in list_of_interns(callback.from_user.username) if i[1] in info[2].split()])
            await callback.message.answer('Задача изменена')
            await callback.message.answer(
                text=f'Название: {info[1]}\n\nСтажеры:\n{interns}\nДедлайн: {'.'.join(info[5].split('-')[::-1])}\nОписание: {
                info[4]}\nФормат отчета: {info[6]}\nСтатус: {"не выполнена" if info[-1] != False else "выполнена"}',
                reply_markup=admin_keyboard)
            await state.set_state(Form.main_admin)
    elif callback.data == 'back':
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Меню команд', callback_data='back')]]))
        await callback.message.answer(text=f'Задача не была изменена',
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


@router.message(Form.change_task_interns)
async def change_task_interns(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


def func_change_task(tasks_id, field, value):
    if change_tasks_info(tasks_id, field, value):
        return True
    return False
