from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .forms import Form
from db.db_request.new_user import is_new_user
from resource.keyboards.admin_keyboard import admin_keyboard
from resource.keyboards.admin_father_keyboard import admin_father_keyboard

import asyncio

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    is_new = is_new_user(message.from_user.id)
    if is_new == 'new':
        await message.answer('''Добро пожаловать!
Данный бот предназначен для упрощения взаимодействия между руководителем и стажерами.
Для дальнейшей работы пройдите регистрацию!''')
        await asyncio.sleep(3)
        await message.answer('Введите ключ, выданный администратором:')
        await state.update_data(login=0)
        await state.set_state(Form.registration_psw)
    else:
        if is_new == 2:
            await message.answer('Вы уже зарегистрированы',
                                 reply_markup=admin_keyboard)
            await state.set_state(Form.main_admin)
        elif is_new == 1:
            await message.answer('Вы уже зарегистрированы',
                                 reply_markup=admin_father_keyboard)
            await state.set_state(Form.main_admin_father)
        else:
            await message.answer('Вы уже зарегистрированы')
            await state.set_state(Form.main_intern)
