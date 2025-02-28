from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .forms import Form
from config import *

import time

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('''Добро пожаловать!
Данный бот предназначен для упрощения взаимодействия между руководителем и стажерами.
Для дальнейшей работы пройдите регистрацию!
    ''')
    time.sleep(3)
    await message.answer('Введите пароль, выданный администратором:')
    await state.set_state(Form.start)


@router.message(Form.start)
async def get_psw(message: Message, state: FSMContext):
    psw = message.text
    if psw == ADMIN_PSW:
        pass
