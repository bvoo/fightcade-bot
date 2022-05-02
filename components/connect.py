import requests
import json
import websocket
import components.message_handler as handler
import logging

api_url = 'https://web.fightcade.com/api/'
ws_url = 'wss://ggs.fightcade.com/ws/'

data = json.dumps({"req":"location"})

r = requests.post(api_url, data=data)
location = r.json()["location"]

with open('./important.json') as f:
    data = json.load(f)

login_data = json.dumps({
    "location": location,
    "req": "login",
    "requestIdx": -1,
    "username": data['username'],
    "userpass": data['password']
})

ws_headers = {
    'User-Agent': data['fightcade_version']
}

on_message = handler.handle_message
on_error = handler.handle_error
on_close = handler.handle_close


def on_open(ws):
    logging.info('Connected to {}'.format(ws.url))
    ws.send(login_data)


def connect():
    ws = websocket.WebSocketApp(ws_url, header=ws_headers, on_message=on_message, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(host='ggs.fightcade.com', origin='https://web.fightcade.com')
