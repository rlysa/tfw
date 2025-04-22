from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.list_of_interns_kb import list_of_interns_select_kb
from db.db_request.create_group import new_group
from db.db_request.list_interns import list_of_interns


router = Router()


@router.message(Form.create_group_name)
async def create_group_get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    interns = func_list_of_interns(message.from_user.username)
    await state.update_data(interns=interns)
    await message.answer('Выберите стажеров из списка. Сделав выбор, нажмите "Далее"',
                         reply_markup=list_of_interns_select_kb(interns, []))
    await state.update_data(selected=[])
    await state.set_state(Form.create_group_interns)


@router.message(Form.create_group_interns)
async def create_group_get_interns(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')


@router.callback_query(Form.create_group_interns)
async def create_group_get_interns(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_interns = data['selected']
    if callback.data == 'next':
        await callback.message.answer(f'Группа "{data['name']}" создана\n\nСтажеры:\n@{'\n@'.join(selected_interns)}',
                                      reply_markup=admin_keyboard)
        create_group(data['name'], callback.from_user.username, selected_interns)
        await state.set_state(Form.main_admin)
    else:
        if callback.data in selected_interns:
            selected_interns.pop(selected_interns.index(callback.data))
        else:
            selected_interns.append(callback.data)
        await state.update_data(selected=selected_interns)
        await callback.message.edit_reply_markup(
            reply_markup=list_of_interns_select_kb(data['interns'], selected_interns))


def create_group(name, admin, interns):
    interns = ' '.join(interns)
    new_group(name, admin, interns)


def func_list_of_interns(admin):
    return list_of_interns(admin)
