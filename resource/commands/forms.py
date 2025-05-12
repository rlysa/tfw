from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start = State()
    block = State()
    main_admin = State()
    main_admin_father = State()
    main_intern = State()

    registration_psw = State()
    registration_surname = State()
    registration_name = State()
    registration_middle_name = State()
    registration_skills = State()

    view_the_task_list = State()
    view_group_composition = State()
    view_my_info = State()
    main_menu = State()
    changing_info = State()

    skill_search = State()
    send_message_text = State()
    send_message_interns = State()

    interns_commands = State()
    look_interns_info = State()
    delete_intern = State()

    look_profile = State()
    change_profile = State()
    change_profile_new = State()

    tasks_commands = State()
    look_tasks = State()

    create_task_name = State()
    create_task_interns = State()
    create_task_description = State()
    create_task_deadline = State()
    create_task_report = State()

    change_delete_task = State()
    change_task = State()
    change_task_new = State()
    change_task_report = State()
    change_task_interns = State()

    groups_commands = State()
    look_groups_info = State()

    create_group_name = State()
    create_group_interns = State()

    change_delete_group = State()
    change_group = State()
    change_group_name = State()
    change_group_interns = State()
