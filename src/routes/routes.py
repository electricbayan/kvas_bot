from aiogram import Router
from aiogram.types import CallbackQuery
from src.message_text import message_text, languages
from api.database.database import Database
from src.keyboards.keyboards import main_menu_kb, offers_kb, help_kb, skin_kb, building_kb, totem_kb, art_kb, three_dim_kb
from src.keyboards.creator_keyboards import main_menu_kb_creator_busy, main_menu_kb_creator
from src.keyboards.admin_kb import main_menu_kb_admin
from aiogram import F
from aiogram.fsm.context import FSMContext
from os import getenv


main_rt = Router()
db = Database()


@main_rt.callback_query(F.data.in_(languages))
async def greeting_msg(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    if str(callback.from_user.id) in getenv('ADMINS_ID'):
        await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=main_menu_kb_admin)
    elif (await db.is_user_creator(str(callback.from_user.id))):
        if await db.is_creator_busy(str(callback.from_user.id)):
            await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=main_menu_kb_creator_busy)
        else:
            await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=main_menu_kb_creator)
    else:
        await callback.message.edit_text(message_text[lang]['greeting'], reply_markup=main_menu_kb)
    await callback.answer('')
    await state.clear()


@main_rt.callback_query(F.data=='offers')
async def services(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['offers'], reply_markup=offers_kb)
    await callback.answer('')
    await state.clear()

@main_rt.callback_query(F.data=='skin_menu')
async def skin_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['skin_menu'], reply_markup=skin_kb)
    await callback.answer('')
    await state.clear()

@main_rt.callback_query(F.data=='building_menu')
async def building_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['building_menu'], reply_markup=building_kb)
    await callback.answer('')
    await state.clear() 

@main_rt.callback_query(F.data=='totem_menu')
async def totem_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['totem_menu'], reply_markup=totem_kb)
    await callback.answer('')
    await state.clear() 

@main_rt.callback_query(F.data=='3d_menu')
async def three_dim_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['3d_menu'], reply_markup=three_dim_kb)
    await callback.answer('')
    await state.clear() 

@main_rt.callback_query(F.data=='art_menu')
async def art_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['art_menu'], reply_markup=art_kb)
    await callback.answer('')
    await state.clear() 

@main_rt.callback_query(F.data=="help")
async def get_help(callback: CallbackQuery):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(message_text[lang]['help'], reply_markup=help_kb)
    await callback.answer('')


@main_rt.callback_query(F.data=="design")
async def design(callback: CallbackQuery):
    # lang = await db.get_language(callback.from_user.id)
    # await callback.message.edit_text(message_text[lang]['help'], reply_markup=help_kb)
    await callback.answer('')