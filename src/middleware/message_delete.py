from aiogram import BaseMiddleware
from aiogram.types import Message
from src.states.payment_states import PaymentState
from typing import Callable, Dict, Any, Awaitable
from api.database.database import Database
from main import bot


class DeleteMessage(BaseMiddleware):
    menu_message_id: int | None = None
    chat_id: int | None = None
    db = Database()
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]):

        is_delete_msg = False
        

        msg_id = await handler(event, data)
        chat_id = data['event_context'].chat.id
        if is_delete_msg:
            self.menu_message_id = msg_id
            self.chat_id = chat_id
        

        if event.text == '/start':
            self.menu_message_id = msg_id
            self.chat_id = chat_id
        else:
            await bot.delete_message(message_id=self.menu_message_id, chat_id=self.chat_id)
            self.menu_message_id = msg_id
            self.chat_id = chat_id

