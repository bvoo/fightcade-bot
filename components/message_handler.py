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
        elif message['user']['role']:
            message['user']['name'] = message['user']['name'].lower()
            roles = {"1": "normal", '10': 'fan', '20': 'supporter', '30': 'hardcore', '40': 'ranked', '50': 'premium', '60': 'vip', '90': 'mod', '100': 'dev'}
            role = roles[str(message['user']['role'])]
            if message['user']['role'] != 1:
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
            logging.info('Rate limited... Pausing for 5s.')
            time.sleep(5)

        try:
            if message['username'] == data['username']:
                return
        except:
            return

        try:
            if handle_chat(message) == True:
                if 'ROM' in message['chat'].upper():
                    msg = '@{}, ROMs can be found at https://krypton.sh/'.format(message['username'])
                    chat.send(ws, msg, message['channelname'], idx)
                elif 'MORBIUS' in message['chat'].upper():
                    msg = '@{}, #MorbiusSweep https://tenor.com/view/morbius-morbius-sweep-gif-25378327 https://cdn.discordapp.com/attachments/950667635723477042/970896014846341171/morbius.mp4'.format(message['username'])
                    chat.send(ws, msg, message['channelname'], idx)
                elif 'WHOIS' in message['chat'].upper():
                    target_user = message['chat'].split(' ')[1]
                    target_user = target_user.lower()
                    with open('./users.json', 'r') as f:
                        users = json.load(f)
                    if target_user in users:
                        msg = '@{}, @{}\'s role is: {}'.format(message['username'], target_user, users[target_user])
                    else:
                        msg = '{} is not in the database (Likely never logged)'.format(target_user)
                    chat.send(ws, msg, message['channelname'], idx)
                elif 'STATS' in message['chat'].upper():
                    with open('./users.json', 'r') as f:
                        users = json.load(f)

                    roles = [
                        {'role': 'normal', 'count': 0},
                        {'role': 'fan', 'count': 0},
                        {'role': 'supporter', 'count': 0},
                        {'role': 'hardcore', 'count': 0},
                        {'role': 'ranked', 'count': 0},
                        {'role': 'premium', 'count': 0},
                        {'role': 'vip', 'count': 0},
                        {'role': 'mod', 'count': 0},
                        {'role': 'dev', 'count': 0}
                    ]

                    for user in users:
                        for role in roles:
                            if users[user] == role['role']:
                                role['count'] += 1
                    
                    msg = '@{}, Here are the current stats: Users in database: {}, Normal users: {}, Fans: {}, Supporters: {}, Hardcore: {}, Ranked: {}, Premium: {}, VIP: {}, Moderators: {}, Developers: {}'.format(message['username'], len(users), roles[0]['count'], roles[1]['count'], roles[2]['count'], roles[3]['count'], roles[4]['count'], roles[5]['count'], roles[6]['count'], roles[7]['count'], roles[8]['count'])

                    chat.send(ws, msg, message['channelname'], idx)
                elif 'HELP' in message['chat'].upper():
                    msg = '@{}, My commands are as follows: !rom(s) !morbius !whois (user) !help'.format(message['username'])
                    chat.send(ws, msg, message['channelname'], idx)
                else:
                    msg = '@{}, {} is an invalid command. Use !help to see my commands.'.format(message['username'], message['chat'].split(' ', 1)[0])
                    chat.send(ws, msg, message['channelname'], idx)
        except Exception as e:
            logging.error('Chat failed: {}'.format(e))
    
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
