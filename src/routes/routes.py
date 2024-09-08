from aiogram import Router
from aiogram.types import CallbackQuery
from src.message_text import message_text, languages
from api.database.database import Database
from src.keyboards.keyboards import main_menu_kb, offers_kb, skin_kb, building_kb, totem_kb, art_kb, three_dim_kb, back_to_main_menu, design_kb, mod_kb
from src.keyboards.creator_keyboards import main_menu_kb_creator_busy, main_menu_kb_creator
from src.keyboards.admin_kb import main_menu_kb_admin
from aiogram import F
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from os import getenv


main_rt = Router()
db = Database()


@main_rt.callback_query(F.data.in_(languages) or F.data == 'main_menu')
async def greeting_msg(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)

    # caption=message_text[lang]['greeting']
    photo = FSInputFile("static/main_menu.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['greeting'], parse_mode="HTML")
    if str(callback.from_user.id) in getenv('ADMINS_ID'):
        await callback.message.edit_media(file, reply_markup=main_menu_kb_admin)
    elif (await db.is_user_creator(str(callback.from_user.id))):
        if await db.is_creator_busy(str(callback.from_user.id)):
            await callback.message.edit_media(file, reply_markup=main_menu_kb_creator_busy)
        else:
            await callback.message.edit_media(file, reply_markup=main_menu_kb_creator)
    else:
        await callback.message.edit_media(file, reply_markup=main_menu_kb)
    await callback.answer('')
    await state.clear()


@main_rt.callback_query(F.data=='offers')
async def services(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/offers.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['offers'], parse_mode="HTML")
    await callback.message.edit_media(file, reply_markup=offers_kb)
    await callback.answer('')
    await state.clear()

@main_rt.callback_query(F.data=='skin_menu')
async def skin_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/skins.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['skin_menu'], parse_mode='HTML')
    await callback.message.edit_media(file, reply_markup=skin_kb)
    await callback.answer('')
    await state.clear()

@main_rt.callback_query(F.data=='building_menu')
async def building_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/buildings.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['building_menu'], parse_mode="HTML")
    await callback.message.edit_media(file, reply_markup=building_kb)
    await callback.answer('')
    await state.clear() 

@main_rt.callback_query(F.data=='totem_menu')
async def totem_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/totems.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['totem_menu'], parse_mode="HTML")
    await callback.message.edit_media(file, reply_markup=totem_kb)
    await callback.answer('')
    await state.clear() 

@main_rt.callback_query(F.data=='3d_menu')
async def three_dim_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/threedim.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['3d_menu'], parse_mode="HTML")
    await callback.message.edit_media(file, reply_markup=three_dim_kb)
    await callback.answer('')
    await state.clear() 

@main_rt.callback_query(F.data=='art_menu')
async def art_menu(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/art.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['art_menu'], parse_mode="HTML")
    await callback.message.edit_media(file, reply_markup=art_kb)
    await callback.answer('')
    await state.clear() 

@main_rt.callback_query(F.data == 'my_orders')
async def my_orders(callback: CallbackQuery):
    orders = await db.get_user_orders(str(callback.from_user.id))

    msg_text = 'Ваши заказы:\n'
    for num, offer in zip(range(1, 100), orders):
        msg_text += f'{num}. {offer.description}\nID: {offer.token}\n'

    await callback.message.edit_caption(caption=msg_text, reply_markup=back_to_main_menu)
    await callback.answer('')

@main_rt.callback_query(F.data == 'work')
async def work(callback: CallbackQuery):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/work.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['work'])
    await callback.message.edit_media(file, reply_markup=back_to_main_menu)
    await callback.answer('')

@main_rt.callback_query(F.data == 'design')
async def design_offers(callback: CallbackQuery):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/design.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['design'])
    await callback.message.edit_media(file, reply_markup=design_kb)
    await callback.answer('')

@main_rt.callback_query(F.data=='mod')
async def mod_menu(callback: CallbackQuery):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/mod.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['mod'], parse_mode="HTML")
    await callback.message.edit_media(file, reply_markup=mod_kb)
    await callback.answer('')