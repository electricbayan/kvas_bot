from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from src.states.payment_states import PaymentState
from typing import Callable, Dict, Any, Awaitable
from api.database.database import Database


class DeleteMessage(BaseMiddleware):
    menu_message_id: int
    chat_id: int
    db = Database()
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]):
        msg_id = await handler(event, data)
        print('STATE:', await data['state'].get_state())
        if await data['state'].get_state() == PaymentState.description:
            message_to_delete = Message(message_id=self.menu_message_id, chat=self.chat_id)
            message_to_delete.delete()

        if isinstance(event, CallbackQuery):
            print(1)
            if event.data in('drawing_offer', '3d_offer', 'resourses_offer', 'mods_offer'):
                self.menu_message_id = msg_id
                self.chat_id = data['event_chat'].id

            if event.data == "ru":
                await self.db.insert_user(tg_id=str(event.from_user.id), lang="ru")
            elif event.data == "en":
                await self.db.insert_user(tg_id=str(event.from_user.id), lang="en")
