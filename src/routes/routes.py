from aiogram import Router
from aiogram.types import CallbackQuery
from src.message_text import message_text, languages
from api.database.database import Database
from src.keyboards.keyboards import service_kb, offers_kb, help_kb, offers_kb_admin
from aiogram import F
from os import getenv


main_rt = Router()
db = Database()


@main_rt.callback_query(F.data.in_(languages))
@main_rt.callback_query(F.data.in_(languages))
async def greeting_msg(callback: CallbackQuery):
    # буду обращаться к бд, далее обращение к messages по ru[msg]
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=service_kb)
    await callback.answer('')



@main_rt.callback_query(F.data=='offers')
async def services(callback: CallbackQuery):
    lang = await db.get_language(callback.from_user.id)
    if callback.from_user.id in getenv('ADMINS_ID'):
        await callback.message.edit_text(message_text[lang]['offers'], reply_markup=offers_kb_admin)
    else:
        await callback.message.edit_text(message_text[lang]['offers'], reply_markup=offers_kb)
    await callback.answer('')


@main_rt.callback_query(F.data=="help")
async def get_help(callback: CallbackQuery):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['help'], reply_markup=help_kb)
    await callback.answer('')


@main_rt.callback_query(F.data=="help")
async def get_help(callback: CallbackQuery):
    # lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text['ru']['help'], reply_markup=help_kb)
    await callback.answer('')