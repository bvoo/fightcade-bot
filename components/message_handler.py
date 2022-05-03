import json
import components.join as join
import components.chat as chat
import logging
import webbrowser

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
            if message['username'] == data['username']:
                return
        except:
            pass

        try:
            if handle_chat(message) == True:
                msg = '@{}, ROMs can be found at https://krypton.sh/'.format(message['username'])
                chat.send(ws, msg, message['channelname'], idx)
        except Exception as e:
            # dont know what this error is
            if e == 'username':
                pass
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
    if message['chat'][0] != '!':
            return
    logging.info('Command: {} sent by {} in {}'.format(message['chat'], message['username'], message['channelname']))
    if 'ROM' in message['chat'].upper():
        return True
    return False
