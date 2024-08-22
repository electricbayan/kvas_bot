from aiogram import Router
from aiogram.types import CallbackQuery, Message
from api.database.database import Database
from src.keyboards.payment_kb import payment_kb, payment_back_kb
from aiogram import F
from src.states.payment_states import PaymentState
from aiogram.fsm.context import FSMContext
from api.donalerts.token_creator import create_token


payment_rt = Router()
db = Database()
        

@payment_rt.callback_query(F.data.in_(('drawing_skill', '3d_skill', 'resourses_skill', 'mods_skill')))
async def get_payment_link(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("""Опишите ваши требования к заказу""", reply_markup=payment_back_kb)
    
    await state.set_state(PaymentState.description)
    await state.update_data(tg_id=callback.from_user.id)
    await state.update_data(offer_type=callback.data)
    await callback.answer('')


@payment_rt.message(PaymentState.description)
async def get_payment_link(message: Message, state: FSMContext):
    token = await create_token()
    print(token)
    await message.answer(f"""Перейдите по ссылке и оплатите заказ. Позже с вами свяжется исполнитель. \nВАЖНО!\nВставьте в текст сообщения ID своего заказа: \n{token}""", reply_markup=payment_kb)
    userdata = await state.get_data()
    await db.add_payment(customer_id=str(message.from_user.id), offer_type=userdata['offer_type'], description=message.text, amount=0, token=token)
    # order, cr_id, price = await db.confirm_payment(token)
    # print(price)
    await state.clear()
