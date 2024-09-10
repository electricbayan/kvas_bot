from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


payment_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплатить', url='https://www.donationalerts.com/r/kvas_media')],
    [InlineKeyboardButton(text='Назад', callback_data='offers')]
])

payment_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='offers')]
])