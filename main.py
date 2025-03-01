import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from resource.commands.__routers import *
from db.db_data.__all_models import *


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(registration_router)


def run_db():
    users()
    admins()
    interns()
    groups()
    tasks()


async def main():
    run_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
