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
        
        if await data['state'].get_state() == PaymentState.description:
            # message_to_delete = Message(message_id=self.menu_message_id, chat=self.chat_id)
            # message_to_delete.delete()
            await bot.delete_message(message_id=self.menu_message_id, chat_id=self.chat_id)
            is_delete_msg = True

        msg_id = await handler(event, data)
        chat_id = data['event_context'].chat.id
        if is_delete_msg:
            self.menu_message_id = msg_id
            self.chat_id = chat_id


        # print('STATE:', await data['state'].get_state())
        

        if event.text == '/start':
            if self.chat_id and self.menu_message_id:
                await bot.delete_message(message_id=self.menu_message_id, chat_id=self.chat_id)
            self.menu_message_id = msg_id
            self.chat_id = chat_id

