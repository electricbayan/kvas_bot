from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


lang_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги', callback_data='services'),
    InlineKeyboardButton(text='Курсы', callback_data='courses'),
    InlineKeyboardButton(text='Доступ серв', callback_data='access'),
    InlineKeyboardButton(text='Помощь', callback_data='help')
]])