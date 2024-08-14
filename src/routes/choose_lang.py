from aiogram import Router, types
from aiogram.filters import Command
from src.keyboards.choose_lang_kb import lang_kb
from src.message_text import message_text



lang_rt = Router()

@lang_rt.message(Command("start"))
async def choose_language_message(message: types.Message):
    await message.answer(message_text['choose_language'], reply_markup=lang_kb)
