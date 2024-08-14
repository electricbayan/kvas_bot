from aiogram import Router, types
from aiogram.filters import Command
from src.keyboards.choose_lang_kb import lang_kb



lang_rt = Router()

@lang_rt.message(Command("start"))
async def choose_language_message(message: types.Message):
    await message.answer("""
        Please, choose your language below.
        Пожалуйста, выберите язык.
    """, reply_markup=lang_kb)
