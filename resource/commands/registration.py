from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .forms import Form
from config import *
from db.db_request.new_user import new_user
from db.db_request.is_admins_key import is_admins_key
from db.db_request.get_admins_id import get_admins_id
from ..keyboards.admin_keyboard import admin_keyboard


router = Router()


@router.message(Form.registration_psw)
async def registration_get_psw(message: Message, state: FSMContext):
    if len(message.text) > 30:
        await message.answer('Макс. количество символов: 30\nВведите ключ:')
        return
    data = await state.get_data()
    login = data['login'] + 1
    await state.update_data(login=login)
    psw = message.text
    if login >= 5:
        await message.answer('Количество попыток закончилось. Доступ ограничен')
        await state.set_state(Form.block)
        return
    if psw == ADMIN_FATHER_PSW:
        await state.update_data(role=1)
    elif psw == ADMIN_PSW:
        await state.update_data(role=2)
    elif is_admins_key(psw):
        await state.update_data(admin=psw)
        await state.update_data(role=3)
    else:
        await message.answer('Ключ неверный')
        return
    await message.answer('Введите фамилию:')
    await state.set_state(Form.registration_surname)


@router.message(Form.registration_surname)
async def registration_get_surname(message: Message, state: FSMContext):
    if len(message.text) > 30:
        await message.answer('Макс. количество символов: 30\nВведите фамилию:')
        return
    await state.update_data(surname=message.text)
    await message.answer('Введите имя:')
    await state.set_state(Form.registration_name)


@router.message(Form.registration_name)
async def registration_get_name(message: Message, state: FSMContext):
    if len(message.text) > 30:
        await message.answer('Макс. количество символов: 30\nВведите имя:')
        return
    await state.update_data(name=message.text)
    await message.answer('Введите отчество:')
    await state.set_state(Form.registration_middle_name)


@router.message(Form.registration_middle_name)
async def registration_get_middle_name(message: Message, state: FSMContext):
    if len(message.text) > 30:
        await message.answer('Макс. количество символов: 30\nВведите отчество:')
        return
    await state.update_data(middle_name=message.text)
    data = await state.get_data()
    if data['role'] == 3:
        await message.answer('Укажите ваши скиллы:')
        await state.set_state(Form.registration_skills)
    else:
        add_new_user(message.from_user.id, message.from_user.username, data)
        await message.answer('Регистрация завершена',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)


@router.message(Form.registration_skills)
async def registration_get_skills(message: Message, state: FSMContext):
    if len(message.text) > 300:
        await message.answer('Макс. количество символов: 300\nУкажите ваши скиллы:')
        return
    await message.answer('Прикрепите резюме:')
    await state.update_data(skills=message.text)
    await state.set_state(Form.registration_resume)


@router.message(Form.registration_resume)
async def registration_get_resume(message: Message, state:FSMContext):
    if not message.document:
        await message.answer('Прикрепите резюме в виде файла')
        return

    resume = {
        'type': 'file',
        'file_id': message.document.file_id,
        'file_type': 'document',
    }
    await state.update_data(resume=resume)

    await message.answer('Регистрация завершена')
    bot = Bot(token=TOKEN)
    data = await state.get_data()
    await bot.send_message(text=f'Зарегистрирован новый пользователь: @{message.from_user.username} {data['surname']} {data['name']} {data['middle_name']}',
                           chat_id=get_admins_id(data['admin']))
    await bot.session.close()
    add_new_user(message.from_user.id, message.from_user.username, data)
    await state.set_state(Form.main_intern)


def add_new_user(user_id, username, user):
    new_user(user_id, username, user)
