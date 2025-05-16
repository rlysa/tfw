from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from db.db_request.skill_search import skill_search_interns


router = Router()


@router.message(Form.skill_search)
async def skill_search(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
    else:
        interns_skills = skill_search_interns(message.text, message.from_user.username)
        text = '\n\n'.join(interns_skills) if interns_skills else 'Стажеры с запрашиваемым скиллом не найдены'
        await message.answer(text, reply_markup=admin_keyboard)
    await state.set_state(Form.main_admin)
