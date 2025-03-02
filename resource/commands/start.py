from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .forms import Form
from db.db_request.new_user import is_new_user

import time

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if is_new_user(message.from_user.username):
        await message.answer('''Добро пожаловать!
Данный бот предназначен для упрощения взаимодействия между руководителем и стажерами.
Для дальнейшей работы пройдите регистрацию!''')
        time.sleep(3)
        await message.answer('Введите ключ, выданный администратором:')
        await state.set_state(Form.registration_psw)
    else:
        await message.answer('Вы уже зарегистрированы')
        await state.set_state(Form.main)
