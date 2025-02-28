import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from resource.commands._routers import *


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start_router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
