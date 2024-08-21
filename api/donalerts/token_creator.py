from api.database.database import Database
from random import randint


db = Database()

alphabet = {
    '1': 'Aa',
    '2': 'b',
    '3': 'P',
    '4': '4',
    '5': 'K',
    '6': '?',
    '7': 'Ds',
    '8': 'l',
    '9': 'gK',
    '0': 'n'
}

async def create_token():
    last_token = await db.get_token()
    new_token = str(int(last_token[0]) + randint(1, 30))
    new_token_string = ''
    for i in new_token:
        new_token_string += alphabet[i]
        await db.update_token(new_token)
    return new_token_string
