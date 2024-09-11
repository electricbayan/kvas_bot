from aiogram import Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from api.database.database import Database
from src.keyboards.payment_kb import payment_kb, payment_back_kb
from src.keyboards.keyboards import back_to_main_menu
from aiogram import F
from src.states.payment_states import PaymentState
from aiogram.fsm.context import FSMContext
from api.donalerts.token_creator import create_token
from src.message_text import message_text


payment_rt = Router()
db = Database()
        

@payment_rt.callback_query(F.data.contains('skill'))
async def get_payment_link(callback: CallbackQuery, state: FSMContext):
    if callback.data not in ('building_location_skill', 'single_building_skill', 'mod_skill', 'item_skill'):
        await callback.message.edit_caption(caption="""Опишите ваши требования к заказу""", reply_markup=payment_back_kb)
        
        await state.set_state(PaymentState.description)
        await state.update_data(tg_id=callback.from_user.id)
        await state.update_data(offer_type=callback.data)
    else:
        photo = FSInputFile("static/admin.jpg")
        msg = await callback.message.answer_photo(photo, caption=f"""Для заказа писать администратору: @Mr_Bedrok""", reply_markup=back_to_main_menu)
    await callback.answer('')


@payment_rt.message(PaymentState.description)
async def get_payment_link(message: Message, state: FSMContext):
    photo = FSInputFile("static/payment.jpg")
    token = await create_token()
    msg = await message.answer_photo(photo, caption=f"""Перейдите по ссылке и оплатите заказ. Позже с вами свяжется исполнитель.\n\nТекст заказа: {message.text} \n\nВАЖНО!\n\nВставьте в текст сообщения ID своего заказа: \n{token}""", reply_markup=payment_kb)

    userdata = await state.get_data()
    await db.add_payment(customer_id=str(message.from_user.id), offer_type=userdata['offer_type'], description=message.text, token=token)
    # order, cr_id, price, creator_username = await db.confirm_payment(token)
    # print(price)
    await state.clear()
    await message.delete()
    # return msg.message_id

@payment_rt.callback_query(F.data=='change_text')
async def change_message_text(callback: CallbackQuery):
    pass
