from src.exceptions import WrongNickname
from pyrogram import Client
from os import getenv


async def resolve_username_to_channel_id(username: str) -> int | None:
    if username[0] != '@':
        raise WrongNickname
    pyrogram_client = Client(
    "bot",
    api_id=getenv("API_ID"),
    api_hash=getenv("API_HASH"),
    bot_token=getenv("TG_TOKEN"),
    )
    username=username[1:]
    async with pyrogram_client as app:
        res = await app.get_users(username)
    return res.id