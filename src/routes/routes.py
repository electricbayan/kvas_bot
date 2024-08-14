from aiogram import Router
from aiogram.types import CallbackQuery
from main import bot
from src.message_text import message_text



rus_rt = Router()


@rus_rt.callback_query()
async def greeting_msg(callback: CallbackQuery):
    if callback.data == 'ru':
        bot.send_message(callback.from_user.id, "")
