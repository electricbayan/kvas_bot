from aiogram.fsm.state import State, StatesGroup


class AddAdmin(StatesGroup):
    nick_adding = State()
    nick_removing = State()
    