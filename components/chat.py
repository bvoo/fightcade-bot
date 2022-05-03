import json
import logging

# TODO: figure out why this causes req: broken
def send(ws, msg, channel, idx):
    logging.debug('Sending message: {}'.format(msg))
    ws.send(json.dumps({
        'channelname': channel,
        'chat': msg,
        'req': 'chat',
        'requestIdx': idx
    }))
