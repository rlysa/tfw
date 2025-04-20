import asyncio

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
dp.include_router(view_the_task_list_router)
dp.include_router(view_task_description_router)
dp.include_router(view_group_composition_router)
dp.include_router(action_selection_menu_router)
dp.include_router(view_check_my_info_router)
dp.include_router(change_my_info_router)


def run_db():
    global_init(DB_NAME)
    if is_new_user('admin') == True:
         new_user('admin', {'role': 2,
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
