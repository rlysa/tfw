from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard


router = Router()


@router.message(Form.look_profile)
async def change_profile(message: Message, state: FSMContext):
    if message.text == 'Изменить':
        await message.answer('В разработке',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    elif message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
