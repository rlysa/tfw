from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.list_of_interns_kb import list_of_interns_kb
from ...keyboards.admin_keyboard import admin_keyboard


router = Router()


@router.message(Form.main_admin)
async def main_admin(message: Message, state: FSMContext):
    if message.text == 'Стажеры':
        list_of_interns_kb(message.from_user.username)
        await message.answer('Список стажеров',
                             reply_markup=list_of_interns_kb(message.from_user.username))
    elif message.text == 'Группы':
        await message.answer('Функция находится в стадии разработки',
                             reply_markup=admin_keyboard)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=admin_keyboard)
