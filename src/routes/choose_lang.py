from aiogram import Router, types
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from src.keyboards.choose_lang_kb import lang_kb
from src.message_text import message_text
from aiogram import F


lang_rt = Router()

@lang_rt.message(Command("start"))
async def choose_language_message(message: types.Message):
    photo = FSInputFile("static/lang.jpg")
    msg = await message.answer_photo(photo, caption=message_text['choose_language'], reply_markup=lang_kb)
    await message.delete()
    return msg.message_id


@lang_rt.callback_query(F.data=="choose_lang")
async def choose_language_message(callback: types.CallbackQuery):
    photo = FSInputFile("static/lang.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text['choose_language'])
    await callback.message.edit_media(file, reply_markup=lang_kb)
