from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


offers_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Рисование', callback_data='drawing_skill'),
    InlineKeyboardButton(text='3D', callback_data='3d_skill')],
    [InlineKeyboardButton(text='Моды', callback_data='mods_skill'),
     InlineKeyboardButton(text='Ресурспаки', callback_data="resources_skill")],
    [InlineKeyboardButton(text='Назад', callback_data='ru')
]])

service_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги', callback_data='offers'),
    InlineKeyboardButton(text='Курсы', callback_data='courses')],
    [InlineKeyboardButton(text='Доступ серв', callback_data='access'),
    InlineKeyboardButton(text='Помощь', callback_data='help')],
    [InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])

help_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Работа у нас', callback_data='work'),
    InlineKeyboardButton(text='Служба поддержки', callback_data='office')],
    [InlineKeyboardButton(text='Информация', callback_data='info'),
     InlineKeyboardButton(text='Назад', callback_data='ru')
]])
