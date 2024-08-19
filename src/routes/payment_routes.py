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


payment_rt = Router()
db = Database()
        

@payment_rt.callback_query(F.data.in_(('drawing_offer', '3d_offer', 'resourses_offer', 'mods_offer')))
async def add_payment(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ник пользователя (через @)", reply_markup=admin_back_kb)
    if str(callback.from_user.id) in getenv("ADMINS_ID"):
        if callback.data == 'add_creator':
            await state.set_state(AddCreator.nick_adding)
        else:
            await state.set_state(AddCreator.nick_removing)
    await callback.answer('')


