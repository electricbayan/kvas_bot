from aiogram import Router
from aiogram.types import CallbackQuery, Message
from src.message_text import message_text
from api.database.database import Database
from src.keyboards.admin_kb import main_menu_kb_admin, admin_back_kb, adding_skills_admin
from src.keyboards.keyboards import back_to_main_menu
from aiogram import F
from os import getenv
from src.states.admin_states import AddCreator
from aiogram.fsm.context import FSMContext
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid, UsernameNotOccupied
from api.database.database import UserNotFound
from src.telegram_functions import resolve_username_to_channel_id


creator_rt = Router()
db = Database()
        

@creator_rt.callback_query(F.data.in_(('add_creator', 'remove_creator')))
async def add_creator(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ник пользователя (через @)", reply_markup=admin_back_kb)
    if str(callback.from_user.id) in getenv("ADMINS_ID"):
        if callback.data == 'add_creator':
            await state.set_state(AddCreator.nick_adding)
        else:
            await state.set_state(AddCreator.nick_removing)
    await callback.answer('')


@creator_rt.message(AddCreator.nick_adding)
async def creator_adding(message: Message, state: FSMContext):
    try:
        userid = await resolve_username_to_channel_id(message.text.strip())
        await message.answer('Выберите навык исполнителя из списка', reply_markup=adding_skills_admin)
        await state.update_data(userid=userid)
        await state.set_state(AddCreator.skills_adding)
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
        await state.clear()
        await message.answer(message_text['ru']['greeting'], reply_markup=back_to_main_menu)


@creator_rt.callback_query(AddCreator.skills_adding)
async def creator_added(callback: CallbackQuery, state: FSMContext):
    userdata = await state.get_data()
    userid = str(userdata['userid'])
    skill = callback.data
    await callback.message.delete()
    if callback.data == 'skin_skill':
        await db.add_creator(userid, 'vanil_skin_skill')
        await db.add_creator(userid, 'pastel_skin_skill')
    elif callback.data == '3d_skill':
        await db.add_creator(userid, 'mob_skill')
        await db.add_creator(userid, 'item_skill')
    elif callback.data == 'building_skill':
        await db.add_creator(userid, 'building_location_skill')
        await db.add_creator(userid, 'single_building_skill')
    elif callback.data == 'totem3d_skill':
        await db.add_creator(userid, '3d_totem_skill')
    elif callback.data == 'totem2d_skill':
        await db.add_creator(userid, '2d_totem_skill')
    elif callback.data == 'art_skill':
        await db.add_creator(userid, 'art_with_background_skill')
        await db.add_creator(userid, 'art_without_background_skill')
    elif callback.data == 'mod_skill':
        await db.add_creator(userid, 'mod_skill')
    await callback.message.answer(message_text['ru']['greeting'], reply_markup=main_menu_kb_admin)
    await callback.answer('')
    await state.clear()


@creator_rt.message(AddCreator.nick_removing)
async def creator_removed(message: Message, state: FSMContext):

    try:
        userid = await resolve_username_to_channel_id(message.text.strip())
        await db.remove_creator(str(userid)) 
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
    except UserNotFound:
        await message.answer('Пользователь не найден')
    await message.answer(message_text['ru']['greeting'], reply_markup=main_menu_kb_admin)
    await state.clear()

@creator_rt.callback_query(F.data == 'start_offers')
async def start_offers(callback: CallbackQuery):
    await callback.message.edit_text('Теперь вы принимаете заказы.', reply_markup=back_to_main_menu)
    await db.change_creator_business(str(callback.from_user.id), False)
    await callback.answer('')


@creator_rt.callback_query(F.data == 'stop_offers')
async def start_offers(callback: CallbackQuery):
    await callback.message.edit_text('Теперь вы не принимаете заказы.', reply_markup=back_to_main_menu)
    await db.change_creator_business(str(callback.from_user.id), True)
    await callback.answer('')

@creator_rt.callback_query(F.data=='my_offers')
async def my_offers_list(callback: CallbackQuery):
    offers_list = await db.get_creator_offers(str(callback.from_user.id))
    msg_text = 'Ваши заказы:\n'
    for num, offer in zip(range(1, 100), offers_list):
        msg_text += f'{num}. {offer.description}\n'

    await callback.answer('')
    await callback.message.edit_text(msg_text, reply_markup=back_to_main_menu)
