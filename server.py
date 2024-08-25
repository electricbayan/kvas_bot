import json
import socketio
from os import getenv
from pyrogram.client import Client
from api.database.database import Database
from main import bot
import asyncio


class WrongNickname(Exception):
    pass


def resolve_username_to_channel_id(username: str) -> int | None:
    if username[0] != '@':
        raise WrongNickname
    pyrogram_client = Client(
    "bot",
    api_id=getenv("API_ID"),
    api_hash=getenv("API_HASH"),
    bot_token=getenv("TG_TOKEN"),
    )
    username=username[1:]
    with pyrogram_client as app:
        res = app.get_users(username)
    return res.id

db = Database()
sio = socketio.AsyncClient(reconnection=True)
client_id = getenv('DA_ID')
client_secret=getenv("DA_TOKEN")

@sio.on('connect')
async def connect():
    print('connection established')
    await sio.emit('add-user', {'token': 'Sm51ybwsZLyUCNJcrQUC', "type": "alert_widget"})

@sio.event
async def donation(data):
    data = json.loads(data)
    purchase_token = data['message']
    amount = data['amount']
    order, creator_id, price = await db.confirm_payment(purchase_token)

    if float(amount) >= float(price):
        if creator_id:
            await bot.send_message(order.customer_id, f'Заказ принят!\nID: {purchase_token}')
            await bot.send_message(int(creator_id[0]), f'Поступил заказ: {order.description}')
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