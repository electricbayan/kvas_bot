from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


service_kb_creator = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги', callback_data='offers'),
    InlineKeyboardButton(text='Курсы', callback_data='courses')],
    [InlineKeyboardButton(text='Доступ серв', callback_data='access'),
    InlineKeyboardButton(text='Помощь', callback_data='help')],
     [InlineKeyboardButton(text='Мои заказы', callback_data='my_offers'),
      InlineKeyboardButton(text='Остановить приём заказов', callback_data='stop_offers')],
    [InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])


service_kb_creator_busy = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги', callback_data='offers'),
    InlineKeyboardButton(text='Курсы', callback_data='courses')],
    [InlineKeyboardButton(text='Доступ серв', callback_data='access'),
    InlineKeyboardButton(text='Помощь', callback_data='help')],
     [InlineKeyboardButton(text='Мои заказы', callback_data='my_offers'),
      InlineKeyboardButton(text='Начать приём заказов', callback_data='start_offers')],
    [InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])

back_to_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='ru')]
])
