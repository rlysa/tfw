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
dp.include_router(create_task_router)
# dp.include_router(accept_new_user_router)


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
