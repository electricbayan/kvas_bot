from aiogram import Router
from aiogram.types import CallbackQuery
from src.message_text import message_text



main_rt = Router()


@main_rt.callback_query()
async def greeting_msg(callback: CallbackQuery):
    # буду обращаться к бд, далее обращение к messages по ru[msg]
    if callback.data == 'ru':
        await callback.message.edit_text(message_text['ru']['greeting'])


    await callback.answer('')
