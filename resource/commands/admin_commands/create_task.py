from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.list_of_interns_kb import list_of_interns_select_kb
from ...keyboards.back_button import back_kb
from db.db_request.create_task import new_task
from db.db_request.list_interns import list_of_interns
from config import *


router = Router()


@router.message(Form.create_task_name)
async def create_task_get_name(message: Message, state: FSMContext):
    if len(message.text) > 30:
        await message.answer('Макс. количество символов: 30\nВведите название задачи:',
                             reply_markup=back_kb)
        return
    if message.text == 'Меню команд':
        await message.answer('Задача не создана',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
        return
    await state.update_data(name=message.text)
    interns = func_list_of_interns(message.from_user.username)
    await state.update_data(interns=interns)
    await message.answer('Выберите стажеров из списка. Сделав выбор, нажмите "Далее"',
                         reply_markup=list_of_interns_select_kb(interns, []))
    await state.update_data(selected=[])
    await state.set_state(Form.create_task_interns)


@router.message(Form.create_task_interns)
async def create_task_get_interns(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос',
                         reply_markup=back_kb)


@router.callback_query(Form.create_task_interns)
async def create_task_get_interns(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_interns = data['selected']
    if callback.data == 'next':
        await callback.message.answer('Введите описание задачи:',
                                      reply_markup=back_kb)
        await state.set_state(Form.create_task_description)
    elif callback.data == 'back':
        bot = Bot(token=TOKEN)
        await bot.send_message(callback.from_user.id,
                               text=f'Задача не создана',
                               reply_markup=admin_keyboard)
        await bot.session.close()
        await state.set_state(Form.main_admin)
    else:
        if callback.data in selected_interns:
            selected_interns.pop(selected_interns.index(callback.data))
        else:
            selected_interns.append(callback.data)
        await state.update_data(selected=selected_interns)
        await callback.message.edit_reply_markup(
            reply_markup=list_of_interns_select_kb(data['interns'], selected_interns))


@router.message(Form.create_task_description)
async def create_task_get_description(message: Message, state: FSMContext):
    if len(message.text) > 3000:
        await message.answer('Макс. количество символов: 3000\nВведите описание задачи:',
                             reply_markup=back_kb)
        return
    if message.text == 'Меню команд':
        await message.answer('Задача не создана',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
        return
    await state.update_data(description=message.text)
    await message.answer('Укажите сроки выполнения задачи в формате дд.мм.гггг:',
                         reply_markup=back_kb)
    await state.set_state(Form.create_task_deadline)


@router.message(Form.create_task_deadline)
async def create_task_get_deadline(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Задача не создана',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
        return
    try:
        if (datetime.strptime(message.text, "%d.%m.%Y").date() - datetime.today().date()).days < 1:
            await message.answer('Срок выполнения может быть назначен не ранее чем на завтра. Укажите сроки выполнения задачи в формате дд.мм.гггг:',
                                 reply_markup=back_kb)
        else:
            await state.update_data(deadline=datetime.strptime(message.text, "%d.%m.%Y").date())
            await message.answer('Укажите формат отчета о выполнении задач (мб тоже список)',
                                 reply_markup=back_kb)
            await state.set_state(Form.create_task_report)
    except Exception as e:
        await message.answer('Дата указана неверно. Укажите сроки выполнения задачи в формате дд.мм.гггг:',
                             reply_markup=back_kb)


@router.message(Form.create_task_report)
async def create_task_get_report(message: Message, state: FSMContext):
    if len(message.text) > 30:
        await message.answer('Макс. количество символов: 30\nУкажите формат отчета о выполнении задач',
                             reply_markup=back_kb)
        return
    if message.text == 'Меню команд':
        await message.answer('Задача не создана',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
        return
    await state.update_data(report=message.text)
    data = await state.get_data()
    create_task(data, message.from_user.username)
    await message.answer('Задача создана', reply_markup=admin_keyboard)
    await state.set_state(Form.main_admin)


def create_task(task, admin):
    new_task(task, admin)


def func_list_of_interns(admin):
    return list_of_interns(admin)
