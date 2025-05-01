from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..forms import Form
from db.db_request.list_tasks import list_of_tasks, tasks_info_admin
from db.db_request.list_interns import list_of_interns
from ...keyboards.admin_keyboard import admin_keyboard
from ...keyboards.change_task_group_profile_kb import change_delete_ikb


router = Router()


@router.callback_query(Form.look_tasks)
async def look_tasks(callback: CallbackQuery, state: FSMContext):
    list_tasks = '\n'.join([i[1] for i in list_of_tasks(callback.from_user.username)])
    if callback.data == 'back':
        await callback.message.delete()
        await callback.message.answer(text=f'Список задач:\n\n{list_tasks}',
                                      reply_markup=admin_keyboard)
        await state.set_state(Form.main_admin)
    else:
        task = callback.data
        info = tasks_info_admin(task)
        interns = '\n'.join([' - @'.join(i) for i in list_of_interns(callback.from_user.username) if i[1] in info[2].split()])
        await callback.message.edit_text(text=f'Список задач:\n\n{list_tasks}')
        await callback.message.answer(text=f'Название: {info[1]}\n\nСтажеры:\n{interns}\nДедлайн: {'.'.join(info[5].split('-')[::-1])}\nОписание: {
        info[4]}\nФормат отчета: {info[6]}\nСтатус: {"не выполнена" if info[-1] != False else "выполнена"}',
                                      reply_markup=change_delete_ikb)
        await state.set_state(Form.change_delete_task)
        await state.update_data(task=info[0])


@router.message(Form.look_tasks)
async def look_tasks(message: Message, state: FSMContext):
    await message.answer('Некорректный запрос')
