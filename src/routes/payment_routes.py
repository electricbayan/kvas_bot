from aiogram import Router
from aiogram.types import CallbackQuery, Message
from src.message_text import message_text
from api.database.database import Database
from src.keyboards.keyboards import service_kb_admin, admin_back_kb, adding_skills_admin
from src.keyboards.payment_kb import payment_kb, payment_back_kb
from aiogram import F
from os import getenv
from src.states.payment_states import PaymentState
from aiogram.fsm.context import FSMContext
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid, UsernameNotOccupied
from api.database.database import UserNotFound
from src.telegram_functions import resolve_username_to_channel_id


payment_rt = Router()
db = Database()
        

@payment_rt.callback_query(F.data.in_(('drawing_offer', '3d_offer', 'resourses_offer', 'mods_offer')))
async def get_payment_link(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("""Опишите ваши требования к заказу""", reply_markup=payment_back_kb)
    
    await state.set_state(PaymentState.description)
    await state.update_data(tg_id=callback.from_user.id)
    await state.update_data(offer_type=callback.data)
    await callback.answer('')


@payment_rt.message(PaymentState.description)
async def get_payment_link(message: Message, state: FSMContext):
    await message.answer("""Перейдите по ссылке и оплатите заказ. Позже с вами свяжется исполнитель.""", reply_markup=payment_kb)
    
    userdata = await state.get_data()
    await db.add_payment(str(message.from_user.id), userdata['offer_type'], message.text, amount=0)
    await state.clear()
