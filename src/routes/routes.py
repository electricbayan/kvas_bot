from aiogram import Router
from aiogram.types import CallbackQuery
from src.message_text import message_text, languages
from api.database.database import Database
from src.keyboards.keyboards import service_kb, offers_kb, help_kb
from src.keyboards.creator_keyboards import service_kb_creator, service_kb_creator_busy
from src.keyboards.admin_kb import service_kb_admin
from aiogram import F
from aiogram.fsm.context import FSMContext
from os import getenv


main_rt = Router()
db = Database()


@main_rt.callback_query(F.data.in_(languages))
async def greeting_msg(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    if str(callback.from_user.id) in getenv('ADMINS_ID'):
        await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=service_kb_admin)
    elif (await db.is_user_creator(str(callback.from_user.id))):
        # print(db.is_user_creator(callback.from_user.id))
        if await db.is_creator_busy(str(callback.from_user.id)):
            await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=service_kb_creator_busy)
        else:
            await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=service_kb_creator)
    else:
        await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=service_kb)
    await callback.answer('')
    await state.clear()


@main_rt.callback_query(F.data=='offers')
async def services(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['offers'], reply_markup=offers_kb)
    await callback.answer('')
    await state.clear()


@main_rt.callback_query(F.data=="help")
async def get_help(callback: CallbackQuery):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['help'], reply_markup=help_kb)
    await callback.answer('')


