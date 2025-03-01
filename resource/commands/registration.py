from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .forms import Form
from config import *
from db.db_request.new_user import new_user

router = Router()

user = {
    'role': 3,
    'surname': '',
    'name': '',
    'middle_name': '',
    'username': '',
}


@router.message(Form.registration_psw)
async def registration_get_psw(message: Message, state: FSMContext):
    psw = message.text
    global user
    if psw == ADMIN_FATHER_PSW:
        user['role'] = 1
    elif psw == ADMIN_PSW:
        user['role'] = 2
    elif psw == INTERN_PSW:
        user['role'] = 3
    else:
        await message.answer('Ключ неверный:')
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
        await message.answer('Регистрация завершена. Ждите подтверждения')
        await state.set_state(Form.registration_skills)


@router.message(Form.registration_skills)
async def registration_get_skills(message: Message, state: FSMContext):
    user['skills'] = message.text
    add_new_user('11111')
    await message.answer('Регистрация завершена. Ждите подтверждения')
    await state.set_state(Form.registration_skills)


def add_new_user(username):
    global user
    new_user(username, user['role'], user['surname'], user['name'], user['middle_name'])
