from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.list_of_interns_kb import list_of_interns_select_kb
from db.db_request.create_task import new_task


router = Router()


@router.message(Form.create_group_name)
async def create_group_get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Выберите стажеров из списка. Сделав выбор, нажмите "Далее"',
                         reply_markup=list_of_interns_select_kb(message.from_user.username, []))
    await state.update_data(interns=[])
    await state.set_state(Form.create_group_interns)


@router.message(Form.create_group_interns)
async def create_group_get_interns(message: Message, state: FSMContext):
    await message.answer('Группа создана', reply_markup=admin_keyboard)
    await state.set_state(Form.main_admin)


@router.callback_query(Form.create_group_interns)
async def create_group_get_interns(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    interns = data['interns']
    if callback.data == 'next':
        print(interns)
        await callback.message.answer('Группа создана', reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        if callback.data in interns:
            print(interns, callback.data, interns.index(callback.data))
            interns.pop(interns.index(callback.data))
        else:
            print(interns, callback.data)
            interns.append(callback.data)
        await state.update_data(interns=interns)
        await callback.message.edit_reply_markup(reply_markup=list_of_interns_select_kb(callback.from_user.username, interns))


def create_group(group, admin):
    new_task(group, admin)
