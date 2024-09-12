from aiogram import Router
from aiogram.types import CallbackQuery, Message
from src.message_text import message_text
from api.database.database import Database
from src.keyboards.admin_kb import main_menu_kb_admin, admin_back_kb
from aiogram import F
from os import getenv
from src.states.admin_states import AddAdmin
from aiogram.fsm.context import FSMContext
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid, UsernameNotOccupied
from api.database.database import UserNotFound
from aiogram.filters import Command
from src.telegram_functions import resolve_username_to_channel_id


admin_rt = Router()
db = Database()


@admin_rt.callback_query(F.data.in_(('add_admin', 'remove_admin')))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(caption="Введите ник пользователя (через @)", reply_markup=admin_back_kb)
    if str(callback.from_user.id) in getenv("ADMINS_ID"):
        if callback.data == 'add_admin':
            await state.set_state(AddAdmin.nick_adding)
        else:

            await state.set_state(AddAdmin.nick_removing)
    await callback.answer('')


@admin_rt.message(AddAdmin.nick_adding)
async def admin_added(message: Message, state: FSMContext):

    try:
        userid = await resolve_username_to_channel_id(message.text.strip())
        await db.add_admin(str(userid))
        await message.answer('Успешно.')
        await message.answer(message_text['ru']['greeting'], reply_markup=main_menu_kb_admin, parse_mode='HTML')
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
    await state.clear()


@admin_rt.message(AddAdmin.nick_removing)
async def admin_removed(message: Message, state: FSMContext):

    try:
        userid = await resolve_username_to_channel_id(message.text.strip())
        await db.remove_admin(str(userid)) 
        await message.answer('Успешно.')
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
    except UserNotFound:
        await message.answer('Пользователь не найден')
    await message.answer(message_text['ru']['greeting'], reply_markup=main_menu_kb_admin, parse_mode='HTML')
    await state.clear()

@admin_rt.message(Command('profit'))
async def get_profit(message: Message):
    if str(message.from_user.id) in getenv("ADMINS_ID"):
        creators_profit = await db.get_profit()
        final_message=''
        for orderid, creator_id in enumerate(creators_profit.keys()):
            final_message += f'{orderid}. {creator_id}: {creators_profit[creator_id]}\n'
        await message.answer(final_message)
            