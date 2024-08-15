from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from api.database.database import Database

class InsertUserMiddleware(BaseMiddleware):
    db = Database()
    async def __call__(self, handler,
        event: CallbackQuery,
        data):
        if event.data == "ru":
            await self.db.insert_user(tg_id=str(event.from_user.id), lang="ru")
        elif event.data == "en":
            await self.db.insert_user(tg_id=str(event.from_user.id), lang="en")

        await handler(event, data)
