from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_menu_kb_creator = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги майнкрафт', callback_data='offers'),
    InlineKeyboardButton(text='Дизайн', callback_data='design')],
    [InlineKeyboardButton(text="Мои заказы", callback_data="my_offers"),
     InlineKeyboardButton(text='Остановить прием заказов', callback_data='stop_offers')],
    [InlineKeyboardButton(text='Помощь', callback_data='help'),
    InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])


main_menu_kb_creator_busy = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги майнкрафт', callback_data='offers'),
    InlineKeyboardButton(text='Дизайн', callback_data='design')],
    [InlineKeyboardButton(text="Мои заказы", callback_data="my_offers"),
     InlineKeyboardButton(text='Начать прием заказов', callback_data='start_offers')],
    [InlineKeyboardButton(text='Помощь', callback_data='help'),
    InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])

