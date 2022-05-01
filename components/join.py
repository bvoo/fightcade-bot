import json

channels = [
    "The King of Fighters '98 - The Slugfest / King of Fighters '98 - dream match never ends (NGM-2420)",
    "The King of Fighters 2002 (NGM-2650)",
    "Street Fighter III 3rd Strike: Fight for the Future (Japan 990512, NO CD)"
]

def join_channel(ws, channel):
    print("Attemption to join channel {}".format(channel))
    ws.send(json.dumps({
        'away': 'false',
        'channelname': channel,
        'idx': -1,
        'req': 'join',
        'requestIdx': -1,
        'status': 'available'
    }))

def join_channels(ws):
    # TODO: Check account for channel limit
    for channel in channels:
        join_channel(ws, channel)
