from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .forms import Form
from config import *
from db.db_request.new_user import new_user
from db.db_request.is_admins_key import is_admins_key
from db.db_request.get_admins_id import get_admins_id
from ..keyboards.admin_keyboard import admin_keyboard
from ..keyboards.accept_new_user import accept_new_user_kb

router = Router()

user = {
    'role': 3,
    'surname': '',
    'name': '',
    'middle_name': '',
    'admin': '',
    'login': 0
}


@router.message(Form.registration_psw)
async def registration_get_psw(message: Message, state: FSMContext):
    psw = message.text
    global user
    user['login'] += 1
    if user['login'] >= 5:
        await message.answer('Количество попыток закончилось. Доступ ограничен')
        await state.set_state(Form.block)
        return
    if psw == ADMIN_FATHER_PSW:
        user['role'] = 1
    elif psw == ADMIN_PSW:
        user['role'] = 2
    elif is_admins_key(psw):
        user['admin'] = psw
        user['role'] = 3
    else:
        await message.answer('Ключ неверный')
        return
    await message.answer('Введите фамилию:')
    await state.set_state(Form.registration_surname)


@router.message(Form.registration_surname)
async def registration_get_surname(message: Message, state: FSMContext):
    user['surname'] = message.text
    await message.answer('Введите имя:')
    await state.set_state(Form.registration_name)


@router.message(Form.registration_name)
async def registration_get_name(message: Message, state: FSMContext):
    user['name'] = message.text
    await message.answer('Введите отчество:')
    await state.set_state(Form.registration_middle_name)


@router.message(Form.registration_middle_name)
async def registration_get_middle_name(message: Message, state: FSMContext):
    user['middle_name'] = message.text
    if user['role'] == 3:
        await message.answer('Укажите ваши скиллы:')
        await state.set_state(Form.registration_skills)
    else:
        add_new_user(message.from_user.id, message.from_user.username)
        await message.answer('Регистрация завершена (Ждите подтверждения - реализовать)',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)


@router.message(Form.registration_skills)
async def registration_get_skills(message: Message, state: FSMContext):
    user['skills'] = message.text
    await message.answer('Регистрация завершена (Ждите подтверждения - реализовать)')
    bot = Bot(token=TOKEN)
    await bot.send_message(text=f'Пользователь @{message.from_user.username} {user['surname']} {user['name']} {user['middle_name']} хочет зарегистрироваться',
                           chat_id=get_admins_id(user['admin']),
                           reply_markup=accept_new_user_kb)
    await bot.session.close()
    print(0)
    add_new_user(message.from_user.id, message.from_user.username) # делать только после регистрации
    await state.set_state(Form.main_intern)


def add_new_user(user_id, username):
    global user
    new_user(user_id, username, user)
