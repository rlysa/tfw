from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import re

from ..forms import Form
from ...keyboards.admin_keyboard import admin_keyboard
from db.db_request.skill_search import skill_search_interns


router = Router()

def enhance_search_with_regex(skill_query: str, username: str) -> list:
    try:
        pattern = re.compile(rf"\b{re.escape(skill_query)}\b", flags=re.IGNORECASE)
        results = skill_search_interns(skill_query, username)
        return [item for item in results if pattern.search(item)]
    except Exception:
        return skill_search_interns(skill_query, username)

@router.message(Form.skill_search)
async def skill_search(message: Message, state: FSMContext):
    if message.text == 'Меню команд':
        await message.answer('Выберите команду:',
                             reply_markup=admin_keyboard)
    else:
        interns_skills = enhance_search_with_regex(message.text, message.from_user.username)
        text = '\n\n'.join(interns_skills) if interns_skills else 'Стажеры с запрашиваемым скиллом не найдены'
        await message.answer(text, reply_markup=admin_keyboard)
    await state.set_state(Form.main_admin)
