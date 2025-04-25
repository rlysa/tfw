# from aiogram import Router, Bot
# from aiogram.types import CallbackQuery
# from aiogram.fsm.context import FSMContext
#
# from ..forms import Form
# from config import *
# from ...keyboards.admin_keyboard import admin_keyboard
#
#
# router = Router()
#
#
# @router.callback_query(Form.main_admin)
# async def main_admin(callback: CallbackQuery, state: FSMContext):
#     # bot = Bot(token=TOKEN)
#     # mes_text = ' '.join(callback.message.text.split()[:-2])
#     # if callback.data == 'accept':
#     #     await callback.message.delete()
#     #     await bot.send_message(callback.from_user.id,
#     #                            text=mes_text + ' зарегистрирован',
#     #                            reply_markup=admin_keyboard)
#     # elif callback.data == 'reject':
#     #     await callback.message.delete()
#     #     await bot.send_message(callback.from_user.id,
#     #                            text=mes_text + ' не зарегистрирован',
#     #                            reply_markup=admin_keyboard)
#     # await bot.session.close()
