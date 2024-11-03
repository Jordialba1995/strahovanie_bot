import asyncio
import logging
from aiogram import Bot, Dispatcher

from config_reader import config
import handler_main

bot = Bot(token=config.bot_token.get_secret_value())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# turn on logging
logging.basicConfig(level=logging.INFO)


# dispatcher
dp = Dispatcher()


# registraion routers
dp.include_routers(handler_main.router)


if __name__ == '__main__':
    asyncio.run(main())
