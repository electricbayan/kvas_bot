from aiogram import Router
from aiogram.types import CallbackQuery, Message
from src.message_text import message_text, languages
from api.database.database import Database
from src.keyboards.keyboards import service_kb_admin, admin_back_kb
from aiogram import F
from os import getenv
from src.states.admin_states import AddAdmin
from aiogram.fsm.context import FSMContext
from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid, UsernameNotOccupied
from api.database.database import UserNotFound



class WrongNickname(Exception):
    pass


admin_rt = Router()
db = Database()


async def resolve_username_to_channel_id(username: str) -> int | None:
    if username[0] != '@':
        raise WrongNickname
    pyrogram_client = Client(
    "bot",
    api_id=getenv("API_ID"),
    api_hash=getenv("API_HASH"),
    bot_token=getenv("TG_TOKEN"),
    )
    username=username[1:]
    async with pyrogram_client as app:
        res = await app.get_users(username)
    return res.id
        

@admin_rt.callback_query(F.data.in_(('add_admin', 'remove_admin')))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ник пользователя (через @)", reply_markup=admin_back_kb)
    if callback.data == 'add_admin':
        if str(callback.from_user.id) in getenv("ADMINS_ID"):
            await state.set_state(AddAdmin.nick_adding)
    else:
        if str(callback.from_user.id) in getenv("ADMINS_ID"):
            await state.set_state(AddAdmin.nick_removing)
    await callback.answer('')


@admin_rt.message(AddAdmin.nick_adding)
async def admin_added(message: Message, state: FSMContext):
    db = Database()

    try:
        userid = await resolve_username_to_channel_id(message.text.strip())
        await db.add_admin(str(userid))
        await message.answer('Успешно.')
        await message.answer(message_text['ru']['greeting'], reply_markup=service_kb_admin)
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
    await state.clear()


@admin_rt.message(AddAdmin.nick_removing)
async def admin_added(message: Message, state: FSMContext):
    db = Database()

    try:
        userid = await resolve_username_to_channel_id(message.text.strip())
        await db.remove_admin(str(userid)) 
        await message.answer('Успешно.')
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
    except UserNotFound:
        await message.answer('Пользователь не найден')
    await message.answer(message_text['ru']['greeting'], reply_markup=service_kb_admin)
    await state.clear()
