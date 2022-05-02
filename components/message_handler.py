import json
import components.join as join
import components.chat as chat
import logging

with open('./important.json') as f:
    data = json.load(f)

# TODO: Handle this better
idx = 5

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
        handle_chat(message)

    else:
        logging.debug('Received message: {}'.format(message['req']))


def handle_error(ws, message):
    # TODO: Handle this better
    logging.error(message)


def handle_close():
    # TODO: Reconnect
    logging.info('Connection closed')


def handle_login_result(message):
    try:
        if message['result'] == 200:
            logging.info('Logged in successfully as {}'.format(message['username']))
            return True
    except:
        logging.error('Login failed: ', message['error'])
        exit()


def handle_join_result(message):
    try:
        if message['result'] == 200:
            logging.info('Joined channel successfully')
    except:
        logging.error('Join failed: ', message)


def handle_chat(message):
    logging.info('{}: {}'.format(message['username'], message['chat']))
    if 'ROM' in message['chat'].upper():
        logging.debug('rom detected')
        return True
    return False
