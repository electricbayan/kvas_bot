import json
import socketio
from os import getenv
from api.database.database import Database
from main import bot
import asyncio


class WrongNickname(Exception):
    pass


db = Database()
sio = socketio.AsyncClient(reconnection=True)
da_secret = getenv('DA_SECRET')

@sio.on('connect')
async def connect():
    print('connection established')
    await sio.emit('add-user', {'token': da_secret, "type": "alert_widget"})

@sio.event
async def donation(data):
    data = json.loads(data)
    purchase_token = data['message']
    amount = data['amount']
    order, creator_id, price, creator_username = await db.confirm_payment(purchase_token)

    if float(amount) >= float(price):
        if creator_id:
            await bot.send_message(order.customer_id, f'Заказ принят! TG исполнителя: {creator_username}\nID: {purchase_token}, вид заказа: {order.order_type}')
            await bot.send_message(int(creator_id), f'Поступил заказ: {order.description}, ссылка на заказчика: "tg://openmessage?user_id={order.customer_id}". Тип заказа: {order.order_type}')
        else:
            await bot.send_message(order.customer_id, f'Заказ оплачен. Как только наши специалисты освободятся, мы вам напишем\nID: {purchase_token}')
    else:
        await bot.send_message(order.customer_id, f'Неверная сумма оплаты. Обратитесь в техподдержку.\nID: {purchase_token}')

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('wss://socket.donationalerts.ru:443', transports='websocket', wait_timeout=60)
    while True:
        await sio.wait()

if __name__ == "__main__":
    asyncio.run(main())