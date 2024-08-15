from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv
import asyncio
from src.routes.choose_lang import lang_rt
from src.routes.routes import main_rt
import logging
from src.middleware.users import InsertUserMiddleware
from api.database.database import Database


logging.basicConfig(level=logging.INFO)
load_dotenv()
bot = Bot(getenv("TG_TOKEN"))

async def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    await Database.create_tables()
    bot = Bot(getenv("TG_TOKEN"))
    dp = Dispatcher()
    dp.callback_query.middleware(InsertUserMiddleware())
    dp.include_routers(
        lang_rt, main_rt    
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
