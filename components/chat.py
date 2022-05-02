import json

# TODO: figure out why this causes req: broken
def send(ws, msg, channel, idx):
    print('sent message')
    ws.send(json.dumps({
        'channelname': channel,
        'chat': msg,
        'req': 'chat',
        'requestIdx': idx
    }))
    return True