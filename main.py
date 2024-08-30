from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv
import asyncio
from src.routes.choose_lang import lang_rt
from src.routes.routes import main_rt
import logging
from api.database.database import Database
from src.setup_commands import commands
from src.routes.admin_routes import admin_rt
from src.routes.creator_routes import creator_rt
from src.routes.payment_routes import payment_rt
from src.routes.help import help_rt


logging.basicConfig(level=logging.INFO)
load_dotenv()
bot = Bot(getenv("TG_TOKEN"))
db = Database()
async def main():
    logging.basicConfig(level=logging.INFO)
    await Database.create_tables()
    bot = Bot(getenv("TG_TOKEN"))
    # from src.middleware.message_delete import DeleteMessage
    from src.middleware.users import InsertUserMiddleware
    await bot.set_my_commands(commands=commands)

    dp = Dispatcher()
    dp.callback_query.middleware(InsertUserMiddleware())
    # dp.message.middleware(DeleteMessage())
    # dp.callback_query(DeleteMessage())
    dp.include_routers(
        lang_rt, main_rt, admin_rt, creator_rt, payment_rt, help_rt
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())