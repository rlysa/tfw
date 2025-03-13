from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..forms import Form
from db.db_request.delete_user import delete_user


router = Router()


@router.message(Form.main)
async def main(message: Message, state: FSMContext):
    await message.answer('Что-то')
