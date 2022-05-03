import json
import components.join as join
import components.chat as chat
import logging
import webbrowser
import time

with open('./important.json') as f:
    data = json.load(f)

# TODO: Handle this better
idx = 3

# TODO: switchcase this
def handle_message(ws, message):
    message = json.loads(message)
    if message['req'] == 'login':
        if message['username'] == data['username']:
            if handle_login_result(message) == True:
                join.join_channels(ws)
                return
        
    if message['req'] == 'join':
        if 'result' in message:
            handle_join_result(message)
        elif message['user']['role'] != 1:
            roles = {'10': 'fan', '20': 'supporter', '30': 'hardcore', '40': 'ranked', '50': 'premium', '60': 'vip', '90': 'mod', '100': 'dev'}
            role = roles[str(message['user']['role'])]
            logging.info('Unusual user detected: {}. Role: {}'.format(message['user']['name'], role))
            msg = 'Unusual user detected: @{}. Role: {}'.format(message['user']['name'], role)
            chat.send(ws, msg, message['channelname'], idx)
            with open('./users.json', 'r') as f:
                try:
                    users = json.load(f)
                except:
                    users = {}
            if message['user']['name'] not in users:
                users[message['user']['name']] = role
                with open('./users.json', 'w') as f:
                    json.dump(users, f)
            else:
                if users[message['user']['name']] != role:
                    users[message['user']['name']] = role
                    with open('./users.json', 'w') as f:
                        json.dump(users, f)



    if message['req'] == 'chat':
        if 'result' in message:
            return
        if 'isspam' in message:
            time.sleep(5)

        try:
            if message['username'] == data['username']:
                return
        except:
            pass

        try:
            if handle_chat(message) == True:
                if 'ROM' in message['chat'].upper():
                    msg = '@{}, ROMs can be found at https://krypton.sh/'.format(message['username'])
                    chat.send(ws, msg, message['channelname'], idx)
                if 'MORBIUS' in message['chat'].upper():
                    msg = '@{}, #MorbiusSweep https://tenor.com/view/morbius-morbius-sweep-gif-25378327 https://cdn.discordapp.com/attachments/950667635723477042/970896014846341171/morbius.mp4'.format(message['username'])
                    chat.send(ws, msg, message['channelname'], idx)
        except Exception as e:
            logging.error('Chat failed: {} {}'.format(message, e))
    
    else:
        logging.debug('Received message: {}'.format(message['req']))
    
    if message['req'] == 'updateuser':
        logging.debug('Received token: {}'.format(message['user']['token']))
        
        uri = 'fcade://userstatus/stwlan/' + message['user']['token']
        webbrowser.open(uri)

    if message['req'] == 'broken':
        logging.error('Received error: broken')


def handle_error(ws, message):
    # TODO: Handle this better
    logging.error('Handle error: {}'.format(message))


def handle_close(ws, status_code, msg):
    # TODO: Reconnect, figure out why msg and status code are None
    logging.error('Connection closed: {}'.format(msg))
    logging.error('Status code: {}'.format(status_code))


def handle_login_result(message):
    try:
        if message['result'] == 200:
            logging.success('Logged in as {}'.format(message['username']))
            return True
    except:
        logging.error('Login failed: ', message['error'])
        exit()


def handle_join_result(message):
    try:
        if message['result'] == 200:
            logging.success('Joined channel {}'.format(message['channelname']))
    except:
        logging.error('Join failed: ', message)


def handle_chat(message):
    logging.chat('{}: {}'.format(message['username'], message['chat']))
    if message['chat'][0] == '!':
        logging.info('Command: {} sent by {} in {}'.format(message['chat'], message['username'], message['channelname']))
        return True
    return False
