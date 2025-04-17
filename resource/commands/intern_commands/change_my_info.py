from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.db_request.change_my_info_db import update_user_info, update_intern_skills
from db.db_request.check_my_info import get_full_user_info
from resource.keyboards.change_my_info_kb import get_edit_select_kb, get_back_to_info_kb
from resource.keyboards.check_my_info_kb import get_my_info_kb
from resource.commands.forms import Form
import logging

router = Router(name="change_my_info_router")
logger = logging.getLogger(__name__)

FIELD_NAMES = {
    "surname": "фамилию",
    "name": "имя",
    "middlename": "отчество",
    "skills": "навыки"
}

FIELD_DB_MAPPING = {
    "middlename": "middle_name",
    "skills": "skills"
}


@router.callback_query(F.data == "change_my_info")
async def start_change_info(callback: CallbackQuery, state: FSMContext):
    """Начало изменения данных"""
    await callback.message.edit_text(
        "📝 Выберите что хотите изменить:",
        reply_markup=get_edit_select_kb()
    )
    await state.set_state(Form.changing_info)
    await callback.answer()


@router.callback_query(F.data.startswith("edit_"), Form.changing_info)
async def select_field_to_edit(callback: CallbackQuery, state: FSMContext):
    """Выбор поля для редактирования"""
    field = callback.data.split("_")[1]
    await state.update_data(editing_field=field)

    await callback.message.edit_text(
        f"✏️ Введите новое значение для {FIELD_NAMES.get(field, field)}:",
        reply_markup=get_back_to_info_kb()
    )
    await callback.answer()


@router.message(Form.changing_info)
async def process_field_edit(message: Message, state: FSMContext):
    """Обработка ввода нового значения"""
    user_data = await state.get_data()
    field = user_data.get("editing_field")

    if not field:
        await message.answer("❌ Не выбрано поле для редактирования")
        return

    new_value = message.text.strip()

    if not new_value or len(new_value) > 100:
        await message.answer("❌ Некорректное значение. Длина должна быть от 1 до 100 символов.")
        return

    username = message.from_user.username
    if not username:
        await message.answer("❌ Не удалось определить ваш username")
        return

    if field == "skills":
        success = update_intern_skills(username, new_value)
    else:
        db_field = FIELD_DB_MAPPING.get(field, field)
        success = update_user_info(username, {db_field: new_value})

    if success:
        updated_info = get_full_user_info(username)
        if updated_info:
            from .view_check_my_info import format_complete_user_info
            await message.answer(
                "✅ Данные успешно обновлены!\n\n" +
                format_complete_user_info(updated_info),
                reply_markup=get_my_info_kb()
            )
    else:
        await message.answer(
            "❌ Не удалось обновить данные. Попробуйте позже.",
            reply_markup=get_my_info_kb()
        )

    await state.clear()


@router.callback_query(F.data == "back_to_info", Form.changing_info)
async def back_to_info(callback: CallbackQuery, state: FSMContext):
    """Возврат к просмотру информации"""
    await state.clear()
    username = callback.from_user.username
    if username:
        user_data = get_full_user_info(username)
        if user_data:
            from .view_check_my_info import format_complete_user_info
            await callback.message.edit_text(
                text=format_complete_user_info(user_data),
                reply_markup=get_my_info_kb()
            )
            await callback.answer()
            return

    await callback.message.edit_text(
        text="ℹ️ Используйте /my_info для просмотра данных",
        reply_markup=get_my_info_kb()
    )
    await callback.answer()