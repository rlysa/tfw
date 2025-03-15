from aiogram import Router
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext

from ..forms import Form
from db.db_request.list_interns import interns_info
from ...keyboards.admin_keyboard import admin_keyboard


router = Router()

@router.callback_query(Form.look_interns_info)
async def look_interns_info(callback: CallbackQuery, state: FSMContext):
    username = callback.data
    info = interns_info(username)
    await callback.message.edit_text(text=f'{info[0]}\n\nСкиллы:\n{info[1]}')
    await state.set_state(Form.main_admin)


@router.message(Form.look_interns_info)
async def look_interns_info(message: Message, state: FSMContext):
    if message.text.lower() == 'назад':
        await message.answer('Меню команд',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос')
