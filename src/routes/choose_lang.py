from aiogram import Router, types
from aiogram.filters import Command
from src.keyboards.choose_lang_kb import lang_kb
from src.message_text import message_text
from aiogram import F


lang_rt = Router()

@lang_rt.message(Command("start"))
async def choose_language_message(message: types.Message):
    await message.answer(message_text['choose_language'], reply_markup=lang_kb)
    print(message.message_id)
    await message.delete()


@lang_rt.callback_query(F.data=="choose_lang")
async def choose_language_message(callback: types.CallbackQuery):
    await callback.message.edit_text(message_text['choose_language'], reply_markup=lang_kb)
