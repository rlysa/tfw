import asyncio
import doctest

from aiogram import Bot, Dispatcher

from config import TOKEN
from resource.commands.__routers import *
from db.db_model.db_session import global_init
from db.db_request.new_user import *


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(registration_router)
dp.include_router(admin_main_router)
dp.include_router(look_interns_info_router)
dp.include_router(look_groups_info_router)
# dp.include_router(view_the_task_list_router)
dp.include_router(view_task_description_router)
dp.include_router(view_group_composition_router)
dp.include_router(action_selection_menu_router)
dp.include_router(view_check_my_info_router)
dp.include_router(change_my_info_router)
dp.include_router(create_task_router)
dp.include_router(create_group_router)
dp.include_router(change_profile_router)
dp.include_router(look_tasks_router)
dp.include_router(change_task_router)
dp.include_router(change_group_router)
dp.include_router(skill_search_router)
# dp.include_router(accept_new_user_router)
dp.include_router(task_completion_report_router)
dp.include_router(send_message_router)
dp.include_router(main_admin_father_router)


def run_db():
    global_init(DB_NAME)
    if is_new_user(123567890) == True:
         new_user(123567890,
                  'admin', {'role': 2,
                            'surname': 'Admin',
                            'name': 'Admin',
                            'middle_name': 'Admin',
                            'admin': ''
                            }
                  )  # админ для тестов


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    run_db()
    asyncio.run(main())
