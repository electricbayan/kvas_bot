from aiogram.fsm.state import State, StatesGroup


class PaymentState(StatesGroup):
    tg_id = State()
    offer_type = State()
    description = State()