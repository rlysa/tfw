from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from db.db_request.list_groups import groups_info, list_of_groups
from ...keyboards.admin_keyboard import admin_keyboard
from config import TOKEN


router = Router()


@router.callback_query(Form.look_groups_info)
async def look_groups_info(callback: CallbackQuery, state: FSMContext):
    list_groups = '\n'.join([i[1] for i in list_of_groups(callback.from_user.username)])
    bot = Bot(token=TOKEN)
    if callback.data == 'back':
        await callback.message.delete()
        await bot.send_message(callback.from_user.id,
                               text=f'Список групп:\n\n{list_groups}',
                               reply_markup=admin_keyboard)
    else:
        id = callback.data
        info = groups_info(id)
        info[1] = "\n".join(info[1])
        await callback.message.edit_text(text=f'Список групп:\n\n{list_groups}')
        await bot.send_message(callback.from_user.id,
                               text=f'{info[0]}\n\n{info[1]}',
                               reply_markup=admin_keyboard)
    await bot.session.close()
    await state.set_state(Form.main_admin)


@router.message(Form.look_groups_info)
async def look_groups_info(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')
