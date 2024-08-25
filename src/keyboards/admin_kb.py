from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_menu_kb_admin = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги майнкрафт', callback_data='offers'),
    InlineKeyboardButton(text='Дизайн', callback_data='design')],
    [InlineKeyboardButton(text="Добавить исполнителя", callback_data="add_creator"),
     InlineKeyboardButton(text='Удалить исполнителя', callback_data='remove_creator')],
    [InlineKeyboardButton(text='Мои заказы', callback_data='my_orders')],
    [InlineKeyboardButton(text='Помощь', callback_data='help'),
    InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])

admin_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Назад', callback_data='ru')
    ]
])


adding_skills_admin = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text='Скины', callback_data='skin_skill'), InlineKeyboardButton(text='3D', callback_data='3d_skill')],
        [InlineKeyboardButton(text='Моды', callback_data='mod_skill'), InlineKeyboardButton(text='Постройка', callback_data='building_skill')],
        [InlineKeyboardButton(text='Тотем3D', callback_data='totem3d_skill'), InlineKeyboardButton(text='Тотем2D', callback_data='totem2d_skill')],
        [InlineKeyboardButton(text='Арт', callback_data='art_skill')]
    ]
)