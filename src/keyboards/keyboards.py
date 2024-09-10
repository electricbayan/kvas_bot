from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


offers_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Cкин', callback_data='skin_menu'),
    InlineKeyboardButton(text='Постройка', callback_data='building_menu')],
    [InlineKeyboardButton(text='Мод', callback_data='mod'),
     InlineKeyboardButton(text='Тотем', callback_data="totem_menu")],
    [InlineKeyboardButton(text='3D', callback_data='3d_menu'),
     InlineKeyboardButton(text='Арт', callback_data='art_menu')],
    [InlineKeyboardButton(text='Назад', callback_data='ru'),
]])

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги майнкрафт', callback_data='offers'),
    InlineKeyboardButton(text='Дизайн', callback_data='design')],
    [InlineKeyboardButton(text='Мои заказы', callback_data='my_orders')],
    [InlineKeyboardButton(text='Работа у нас', callback_data='work')],
    [InlineKeyboardButton(text='Помощь', callback_data='help'), 
     InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])

mod_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Заказать мод", callback_data="mod_skill"),
    InlineKeyboardButton(text='Назад', callback_data="offers")
]])

skin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='vanil', callback_data='vanil_skin_skill'),
     InlineKeyboardButton(text='pastel', callback_data='pastel_skin_skill')],
     [InlineKeyboardButton(text='Назад', callback_data='offers')]
])

building_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Локация', callback_data='building_location_skill'),
     InlineKeyboardButton(text='Одиночная постройка', callback_data='single_building_skill')],
     [InlineKeyboardButton(text='Назад', callback_data='offers')]
])

totem_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='2D', callback_data='2d_totem_skill'),
     InlineKeyboardButton(text='3D', callback_data='3d_totem_skill')],
     [InlineKeyboardButton(text='Кастомный', callback_data='custom_totem_skill')],
     [InlineKeyboardButton(text='Назад', callback_data='offers')]
])

art_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='С фоном', callback_data='art_with_background_skill'),
     InlineKeyboardButton(text='Без фона', callback_data='art_without_background_skill')],
     [InlineKeyboardButton(text='Назад', callback_data='offers')]
])

three_dim_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Моб', callback_data='mob_skill'),
     InlineKeyboardButton(text='Предмет', callback_data='item_skill')],
     [InlineKeyboardButton(text='Назад', callback_data='offers')]
])

help_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Работа у нас', callback_data='work'),
    InlineKeyboardButton(text='Служба поддержки', callback_data='office')],
    [InlineKeyboardButton(text='Информация', callback_data='info'),
     InlineKeyboardButton(text='Назад', callback_data='ru')
]])

back_to_main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='ru')]
])

design_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Лого', callback_data='logo_skill'),
     InlineKeyboardButton(text='Оформление', callback_data='registration_skill')],
     [InlineKeyboardButton(text='Назад', callback_data='design')]
])