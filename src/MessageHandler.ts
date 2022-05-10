import consola from 'consola';
import open from 'open';

async function handleMessage(username: string, message: any) {
    let res = {
        req: "",
        channels: []
    }

    switch (message.req) {
        case 'location':
            consola.info(`${username} | Got location`);
            break;
        case 'login':
            if (message['result'] == 200) {
                consola.info(`${username} | Logged in`);
                consola.info(`${username} | Recieved token:`, message['user']['token']);

                let token = message['user']['token'];
                let uri = `fcade://userstatus/stwlan/${token}`;

                open(uri);

                consola.success(`${username} | Opened ${uri}`);

                res.req = 'getLobbies';

                return res
            }
            else {
                consola.error(`${username} | Login failed:`, JSON.stringify(message));
            }
            break;
        case 'error':
            consola.error(`${username} | Error`, message.error);
            break;
        case 'channels':
            consola.info(`${username} | Got channels`);

            res = {
                req: "channels",
                channels: message.channels
            }

            return res;
        case 'join':
            if (message['result'] == 200) {
                consola.info(`${username} | Joined channel:`, message['channelname']);
            }
            else {
                if (message['username'] != username) return;
                consola.error(`${username} | Join failed:`, JSON.stringify(message));
            }
        case 'chat':
            if (!message.username) return;
            // consola.info(`CHAT | ${message.username} | ${message.chat} | ${message.channelname} `);
            if (message.chat.startsWith('!')) {
                res.req = 'command';
                return res;                
            }
        case 'quarkstats':
        case 'challenge':
        case 'cancel':
        case 'stplaying':
        case 'stnoplaying':
        case 'staway':
        case 'stnoaway':
        case 'leave':
        case 'stwlan':
        case 'chaway':
        case 'chnoaway':
        case 'updaterank':
            break;
        default:
            consola.error(`${username} | Unknown message`, message);
    }
}

export default handleMessage;
