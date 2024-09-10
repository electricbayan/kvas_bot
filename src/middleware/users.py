from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from api.database.database import Database
from main import bot
from src.telegram_functions import resolve_username_to_channel_id

class InsertUserMiddleware(BaseMiddleware):
    db = Database()
    async def __call__(self, handler,
        event: CallbackQuery,
        data):
        if event.data == "ru":
            await self.db.insert_user(tg_id=str(event.from_user.id), lang="ru", url=event.from_user.url)
        elif event.data == "en":
            await self.db.insert_user(tg_id=str(event.from_user.id), lang="en", url=event.from_user.url)
        
        message_data = await handler(event, data)
        if message_data:
            creator_username = 'null'
            # creator_username = await resolve_username_to_channel_id(message_data.creator_id)
            await bot.send_message(message_data.creator_id, f"Поступил заказ: {message_data.description}, ссылка на заказчика: 'tg://openmessage?user_id={message_data.customer_id}'. Тип заказа: {message_data.order_type}")
            await bot.send_message(message_data.customer_id, f"Заказ принят! TG исполнителя: {creator_username}\nID: {message_data.token}")
