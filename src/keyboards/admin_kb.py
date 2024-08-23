from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


service_kb_admin = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Услуги', callback_data='offers'),
    # InlineKeyboardButton(text='Курсы', callback_data='courses')
    ],
    [
        # InlineKeyboardButton(text='Доступ серв', callback_data='access'),
    InlineKeyboardButton(text='Помощь', callback_data='help')],
    [InlineKeyboardButton(text='Добавить админа', callback_data="add_admin"), 
     InlineKeyboardButton(text="Добавить исполнителя", callback_data="add_creator")],
     [InlineKeyboardButton(text='Удалить админа', callback_data='remove_admin'),
      InlineKeyboardButton(text='Удалить исполнителя', callback_data='remove_creator')],
    [InlineKeyboardButton(text="Смена языка", callback_data="choose_lang")
]])

admin_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Назад', callback_data='ru')
    ]
])


adding_skills_admin = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text='Рисование', callback_data='drawing_skill'), InlineKeyboardButton(text='3D', callback_data='3d_skill')],
        [InlineKeyboardButton(text='Моды', callback_data='mods_skill'), InlineKeyboardButton(text='Ресурспаки', callback_data='resourcepack_skill')]
    ]
)