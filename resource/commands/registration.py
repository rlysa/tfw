from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .forms import Form
from config import *
from db.db_request.new_user import new_user
from db.db_request.is_admins_key import is_admins_key

router = Router()

user = {
    'role': 3,
    'surname': '',
    'name': '',
    'middle_name': '',
    'admin': '',
}


@router.message(Form.registration_psw)
async def registration_get_psw(message: Message, state: FSMContext):
    psw = message.text
    global user
    if psw == ADMIN_FATHER_PSW:
        user['role'] = 1
    elif psw == ADMIN_PSW:
        user['role'] = 2
<<<<<<< Updated upstream
    elif psw.isdigit():
        if is_admins_key(int(psw)):
            user['admin'] = psw
            user['role'] = 3
=======
    elif psw == INTERN_PSW:
        user['role'] = 3
>>>>>>> Stashed changes
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
        add_new_user(message.from_user.username)
        await message.answer('Регистрация завершена. Ждите подтверждения')
        await state.set_state(Form.registration_skills)


@router.message(Form.registration_skills)
async def registration_get_skills(message: Message, state: FSMContext):
    user['skills'] = message.text
    add_new_user(message.from_user.username)
    await message.answer('Регистрация завершена. Ждите подтверждения')
    await state.set_state(Form.registration_skills)


def add_new_user(username):
    global user
    new_user(username, user)
