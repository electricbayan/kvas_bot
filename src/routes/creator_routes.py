from aiogram import Router
from aiogram.types import CallbackQuery, Message
from src.message_text import message_text, languages
from api.database.database import Database
from src.keyboards.keyboards import service_kb_admin, admin_back_kb
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
async def creator_added(message: Message, state: FSMContext):
    try:
        userid = await resolve_username_to_channel_id(message.text.strip())
        await db.add_creator(str(userid))
        await message.answer('Успешно.')
        await message.answer(message_text['ru']['greeting'], reply_markup=service_kb_admin)
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
    await state.clear()


@creator_rt.message(AddCreator.nick_removing)
async def admin_added(message: Message, state: FSMContext):
    try:
        userid = await resolve_username_to_channel_id(message.text.strip())
        await db.remove_creator(str(userid))
        await message.answer('Успешно.')
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
    except UserNotFound:
        await message.answer('Пользователь не найден')
    await message.answer(message_text['ru']['greeting'], reply_markup=service_kb_admin)
    await state.clear()
