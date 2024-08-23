from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


offers_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Cкин', callback_data='skin_skill'),
    InlineKeyboardButton(text='3D', callback_data='3d_skill')],
    [InlineKeyboardButton(text='Моды', callback_data='mods_skill'),
     InlineKeyboardButton(text='Ресурспаки', callback_data="resources_skill")],
    [InlineKeyboardButton(text='Назад', callback_data='ru')
]])

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги майнкрафт', callback_data='offers'),
    InlineKeyboardButton(text='Дизайн', callback_data='design')
    ],
    [
    # [InlineKeyboardButton(text='Доступ серв', callback_data='access'),
    InlineKeyboardButton(text='Помощь', callback_data='help')
    ],
    [InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])



help_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Работа у нас', callback_data='work'),
    InlineKeyboardButton(text='Служба поддержки', callback_data='office')],
    [InlineKeyboardButton(text='Информация', callback_data='info'),
     InlineKeyboardButton(text='Назад', callback_data='ru')
]])
