import requests
import json
import websocket

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

def connect():
    ws = websocket.WebSocket()
    ws.connect(ws_url, header=ws_headers, host='ggs.fightcade.com', origin='https://web.fightcade.com')
    ws.send(login_data)
    r = json.loads(ws.recv())
    if r['result'] == 200:
        print('Logged in successfully as {}'.format(data['username']))
        return ws
    else:
        print('Login failed: ', r['error'])
        exit()

