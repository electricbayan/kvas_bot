from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


lang_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Русский🇷🇺', callback_data='ru'),
    InlineKeyboardButton(text='English🇬🇧', callback_data='en')
]])

