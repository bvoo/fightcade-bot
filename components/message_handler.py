import json
import components.join as join
import components.chat as chat

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
        print('Received message: ', message['req'])


def handle_error(ws, message):
    # TODO: Handle this better
    print('Error: ', message)


def handle_close():
    # TODO: Reconnect
    print('Connection closed')


def handle_login_result(message):
    try:
        if message['result'] == 200:
            print('Logged in successfully as {}'.format(message['username']))
            return True
    except:
        print('Login failed: ', message['error'])
        exit()


def handle_join_result(message):
    try:
        if message['result'] == 200:
            print('Joined channel successfully')
    except:
        print('Join failed: ', message)


def handle_chat(message):
    print('{}: {}'.format(message['username'], message['chat']))
    if 'ROM' in message['chat'].upper():
        print('rom detected')
        return True
    return False
