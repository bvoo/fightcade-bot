import json

# empty test channel
# "WCW World Championship Wrestling (USA) (NES)",
channels = [
    "JoJo's Bizarre Adventure: Heritage for the Future / JoJo no Kimyou na Bouken: Mirai e no Isan (Japan 990913, NO CD)",
    "Super Street Fighter II X - grand master challenge (super street fighter 2 X 940223 Japan)",
    "Street Fighter III 3rd Strike: Fight for the Future (Japan 990512, NO CD)"
]

def join_channel(ws, channel):
    print("Attempting to join channel {}".format(channel))
    ws.send(json.dumps({
        'away': 'false',
        'channelname': channel,
        'idx': 0,
        'req': 'join',
        'requestIdx': 0,
        'status': 'available'
    }))


def join_channels(ws):
    # TODO: Check account for channel limit
    ws.send(json.dumps({
        "theme": "default", "req": "updateuser", "requestIdx": -1
    }))
    for channel in channels:
        join_channel(ws, channel)
    ws.send(json.dumps({
        "req": "channels", "all": 'true', "requestIdx": 3
    }))
    ws.send(json.dumps({
        "req": "filteroptions", "requestIdx": 4
    }))
