from donationalerts import DonationAlertsAPI, Centrifugo, Scopes, Channels
from flask import Flask, redirect, request
from pprint import pprint
from os import getenv


app = Flask(__name__)


client_id = getenv('DA_ID')
client_secret=getenv("DA_TOKEN")
redirect_uri='http://127.0.0.1:8090/login'
api = DonationAlertsAPI(
    client_id, client_secret, redirect_uri, [Scopes.DONATION_SUBSCRIBE, Scopes.USER_SHOW]
)


@app.route('/')
def index():
    return redirect(api.login())

@app.route('/login')
def login():
    code = request.args.get('code')
    access_token = api.get_access_token(code)
    user = api.user(access_token)
    socket_token = user.socket_connection_token
    user_id = user.id
    fugo = Centrifugo(socket_token, access_token, user_id)
    event = fugo.subscribe(Channels.NEW_DONATION_ALERTS)
    pprint(event)
    return 'ok'

app.run(debug=True, port='8090')