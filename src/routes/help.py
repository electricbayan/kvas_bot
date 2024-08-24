from aiogram import Router
from aiogram.types import CallbackQuery, Message
from src.message_text import message_text
from api.database.database import Database
from src.keyboards.admin_kb import main_menu_kb_admin, admin_back_kb
from aiogram import F
from aiogram.fsm.context import FSMContext
from src.states.admin_states import AddAdmin
from aiogram.fsm.context import FSMContext


help_rt = Router()


@help_rt.callback_query(F.data=='tech_help')
def start_help_dialogue(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Опишите вашу жалобу/вопрос:', reply_markup=)