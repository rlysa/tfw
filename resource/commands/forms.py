from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start = State()
    block = State()
    main_admin = State()
    main_intern = State()

    registration_psw = State()
    registration_surname = State()
    registration_name = State()
    registration_middle_name = State()
    registration_skills = State()

    main_admin = State()
    main_intern = State()
    look_interns_info = State()
    look_groups_info = State()
    view_the_task_list = State()
    view_group_composition = State()
    view_my_info = State()
    main_menu = State()
    changing_info = State()

    create_task_name = State()
    create_task_interns = State()
    create_task_description = State()
    create_task_deadline = State()
    create_task_report = State()

    create_group_name = State()
    create_group_interns = State()
