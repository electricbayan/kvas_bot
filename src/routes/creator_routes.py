from aiogram import Router
from aiogram.types import CallbackQuery, Message
from src.message_text import message_text
from api.database.database import Database
from src.keyboards.keyboards import service_kb_admin, admin_back_kb, adding_skills_admin
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
        await message.answer('Выберите навык исполнителя из списка', reply_markup=adding_skills_admin)
        await state.update_data(userid=userid)
        await state.set_state(AddCreator.skills_adding)
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer('Неверное имя пользователя')
        await state.clear()
        await message.answer(message_text['ru']['greeting'], reply_markup=service_kb_admin)


@creator_rt.callback_query(AddCreator.skills_adding)
async def creator_added(callback: CallbackQuery, state: FSMContext):
    userdata = await state.get_data()
    userid = userdata['userid']
    skill = callback.data
    await callback.message.delete()
    await db.add_creator(str(userid), skill)
    await callback.message.answer('Успешно.')
    await callback.message.answer(message_text['ru']['greeting'], reply_markup=service_kb_admin)
    await callback.answer('')
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
