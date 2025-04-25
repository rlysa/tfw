from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from db.db_request.list_interns import list_of_interns, interns_info
from ...keyboards.admin_keyboard import admin_keyboard
from config import TOKEN


router = Router()


@router.callback_query(Form.look_interns_info)
async def look_interns_info(callback: CallbackQuery, state: FSMContext):
    list_interns = '\n'.join([i[0] for i in list_of_interns(callback.from_user.username)])
    bot = Bot(token=TOKEN)
    if callback.data == 'back':
        await callback.message.delete()
        await bot.send_message(callback.from_user.id,
                               text=f'Список стажеров:\n\n{list_interns}',
                               reply_markup=admin_keyboard)
    else:
        username = callback.data
        info = interns_info(username)
        await callback.message.edit_text(text=f'Список стажеров:\n\n{list_interns}')
        await bot.send_message(callback.from_user.id,
                               text=f'{info[0]}\n@{username}\n\nСкиллы:\n{info[1]}',
                               reply_markup=admin_keyboard)
    await bot.session.close()
    await state.set_state(Form.main_admin)


@router.message(Form.look_interns_info)
async def look_interns_info(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')

