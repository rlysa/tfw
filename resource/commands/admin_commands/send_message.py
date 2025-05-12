from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import TOKEN
from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.list_of_interns_kb import list_of_interns_select_kb, list_of_interns_selected_kb
from ...keyboards.back_button import back_kb
from db.db_request.list_interns import list_of_interns, interns_ids


router = Router()


@router.message(Form.send_message_text)
async def send_message_text(message: Message, state: FSMContext):
    if len(message.text) > 3000:
        await message.answer('Макс. количество символов: 3000\nВведите текст сообщения:',
                             reply_markup=back_kb)
        return
    if message.text == 'Меню команд':
        await message.answer('Сообщение не отправлено',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
        return
    await state.update_data(text=message.text)
    interns = func_list_of_interns(message.from_user.username)
    await state.update_data(interns=interns)
    await message.answer('Выберите стажеров из списка. Сделав выбор, нажмите "Далее"',
                         reply_markup=list_of_interns_select_kb(interns, []))
    await state.update_data(selected=[])
    await state.set_state(Form.send_message_interns)


@router.message(Form.send_message_interns)
async def send_message_interns(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        await message.answer('Некорректный запрос',
                             reply_markup=back_kb)


@router.callback_query(Form.send_message_interns)
async def send_message_interns(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_interns = data['selected']
    if callback.data == 'next':
        await callback.message.edit_reply_markup(
            reply_markup=list_of_interns_selected_kb(data['interns'], selected_interns)
        )
        await callback.message.answer(f'Сообщение отправлено',
                                      reply_markup=admin_keyboard)
        ids = interns_ids(selected_interns)
        bot = Bot(TOKEN)
        for i in ids:
            await bot.send_message(chat_id=i,
                                   text=f'Сообщение от Администратора:\n\n{data['text']}')
        await bot.session.close()
        await state.set_state(Form.main_admin)
    elif callback.data == 'back':
        await callback.message.answer(text=f'Сообщение не отправлено',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        if callback.data in selected_interns:
            selected_interns.pop(selected_interns.index(callback.data))
        else:
            selected_interns.append(callback.data)
        await state.update_data(selected=selected_interns)
        await callback.message.edit_reply_markup(
            reply_markup=list_of_interns_select_kb(data['interns'], selected_interns))


def func_list_of_interns(admin):
    return list_of_interns(admin)
