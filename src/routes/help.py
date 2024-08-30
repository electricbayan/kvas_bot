from aiogram import Router
from aiogram.types import CallbackQuery, Message
from src.message_text import message_text
from api.database.database import Database
from src.keyboards.keyboards import back_to_main_menu
from aiogram import F
from aiogram.fsm.context import FSMContext
from src.states.help_states import HelpState
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext


help_rt = Router()
db = Database()

@help_rt.callback_query(F.data=="help")
async def get_help(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    photo = FSInputFile("static/help.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['help'])
    await callback.message.edit_media(file, reply_markup=back_to_main_menu)
    await callback.answer('')
    await state.set_state(HelpState.msg)

@help_rt.message(HelpState.msg)
async def send_complaint(message: Message, state: FSMContext):
    lang = await db.get_language(message.from_user.id)
    photo = FSInputFile("static/help.jpg")
    file = InputMediaPhoto(media=photo, caption=message_text[lang]['help'])
    await message.answer_photo(file, reply_markup=back_to_main_menu)
    await message.delete()
