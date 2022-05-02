import json
import components.join as join
import components.chat as chat
import logging

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

    if message['req'] == 'chat':
        try:
            if handle_chat(message) == True:
                chat.send(ws, 'ROM', message['channelname'], idx)
        except Exception as e:
            logging.error('Chat failed: {} {}'.format(message, e))
    else:
        logging.debug('Received message: {}'.format(message['req']))
    
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
    if 'ROM' in message['chat'].upper():
        logging.debug('ROM detected in message')
        return True
    return False
