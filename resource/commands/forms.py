from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start = State()
    block = State()
    registration_psw = State()
    registration_surname = State()
    registration_name = State()
    registration_middle_name = State()
    registration_skills = State()
    main = State()
