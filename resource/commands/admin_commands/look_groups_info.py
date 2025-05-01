from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from db.db_request.list_groups import groups_info, list_of_groups
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.change_task_group_profile_kb import change_delete_ikb


router = Router()


@router.callback_query(Form.look_groups_info)
async def look_groups_info(callback: CallbackQuery, state: FSMContext):
    list_groups = '\n'.join([i[1] for i in list_of_groups(callback.from_user.username)])
    if callback.data == 'back':
        await callback.message.delete()
        await callback.message.answer(text=f'Список групп:\n\n{list_groups}',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        groups_id = callback.data
        info = groups_info(groups_id)
        info[1] = "\n".join(info[1])
        await callback.message.edit_text(text=f'Список групп:\n\n{list_groups}')
        await callback.message.answer(text=f'{info[0]}\n\n{info[1]}',
                                      reply_markup=change_delete_ikb)
        await state.set_state(Form.change_delete_group)
        await state.update_data(group=groups_id)


@router.message(Form.look_groups_info)
async def look_groups_info(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')
