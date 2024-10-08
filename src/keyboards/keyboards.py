from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


offers_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Рисование', callback_data='drawing'),
    InlineKeyboardButton(text='3D', callback_data='3d')],
    [InlineKeyboardButton(text='Моды', callback_data='mods'),
     InlineKeyboardButton(text='Ресурспаки', callback_data="resourses")],
    [InlineKeyboardButton(text='Список всех услуг', callback_data='ru')
]])


service_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги', callback_data='offers'),
    InlineKeyboardButton(text='Курсы', callback_data='courses')],
    [InlineKeyboardButton(text='Доступ серв', callback_data='access'),
    InlineKeyboardButton(text='Помощь', callback_data='help')
]])

help_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Работа у нас', callback_data='work'),
    InlineKeyboardButton(text='Служба поддержки', callback_data='office')],
    [InlineKeyboardButton(text='Информация', callback_data='info'),
]])