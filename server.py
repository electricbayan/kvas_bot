from donationalerts import DonationAlertsAPI, Centrifugo, Scopes, Channels
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from os import getenv
from pyrogram.client import Client
from api.database.database import Database
from main import bot


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


app = FastAPI()
db = Database()


client_id = getenv('DA_ID')
client_secret=getenv("DA_TOKEN")
redirect_uri='http://127.0.0.1:8090/login'
api = DonationAlertsAPI(
    client_id, client_secret, redirect_uri, [Scopes.DONATION_SUBSCRIBE, Scopes.USER_SHOW]
)


@app.get('/')
async def index():
    return RedirectResponse(api.login())

@app.get('/login')
async def login(code: str):
    access_token = api.get_access_token(code)
    user = api.user(access_token)
    socket_token = user.socket_connection_token
    user_id = user.id
    fugo = Centrifugo(socket_token, access_token, user_id)
    event = fugo.subscribe(Channels.NEW_DONATION_ALERTS)
    purchase_token = event.message
    print(f'{purchase_token=}')
    order, creator_id, price = await db.confirm_payment(purchase_token)
    print(f'{creator_id=}')
    print(f'{price=}')
    if float(event.amount) >= float(price):
        if creator_id:
            await bot.send_message(order.customer_id, f'Заказ принят!\nID: {purchase_token}')
            await bot.send_message(int(creator_id), f'Поступил заказ: {order.description}')
        else:
            await bot.send_message(order.customer_id, f'Заказ оплачен. Как только наши специалисты освободятся, мы вам напишем\nID: {purchase_token}')
    else:
        await bot.send_message(order.customer_id, f'Неверная сумма оплаты. Обратитесь в техподдержку.\nID: {purchase_token}')

    return RedirectResponse("/")
