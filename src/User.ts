import WebSocket, { RawData } from 'ws';
import req from '@aero/http';
import consola from 'consola';
import handleMessage from './MessageHandler';
import handleCommand from './CommandHandler';

const apiUrl = new URL('https://web.fightcade.com/api');
const wsUrl = new URL('wss://ggs.fightcade.com/ws/');

class User {
    constructor(public username: string, private password: string, public idx: number, public requestIdx: number, public priority: number) {
        this.username = username;
        this.password = password;
        this.idx = idx;
        this.requestIdx = requestIdx;
        this.priority = priority;
        let ws: WebSocket | undefined;

        ws = new WebSocket(wsUrl, {
            headers: { 'User-Agent': 'Fightcade2-WIN32-v2.1.26' },
            origin: "https://web.fightcade.com",
            host: "ggs.fightcade.com"
        });

        this.run(ws);
    }

    public async run(ws: WebSocket): Promise<void> {
        return new Promise(async (resolve, reject) => {
            let location = await this.getLocation();

            consola.info(`${this.username} | Got location`);

            
            // TODO: Figure out why it sometimes doesnt conect
            // let timeout = true;

            // setTimeout(() => {
            //     if (timeout) {
            //         consola.error(`${this.username} | Connection timeout`);
            //         this.run(ws);
            //     }
            // }, 15000);

            ws.on('open', () => {
                // timeout = false;
                consola.success(`${this.username} | Connected to websocket`);
                this.login(ws, location);
            });

            ws.on('error', (err: Error) => {
                consola.error(`${this.username} | Websocket error`, err);
            });

            ws.on('message', async (message: RawData) => {
                const data = JSON.parse(message.toString('utf8'));
                consola.debug(`${this.username} | Got message:`, data['req']);
                let r = await handleMessage(this.username, data);
                if (r) {
                    consola.debug(`${this.username} | Handling message:`, r.req);
                    if (r.req == 'channels') {
                        this.joinLobbies(ws, r.channels);
                    }
                    if (r.req == 'getLobbies') {
                        this.getLobbies(ws);
                    }
                    if (r.req == 'command') {
                        this.handleCommand(ws, data);
                    }
                }
            });

            ws.on('close', () => {
                consola.error(`${this.username} | Websocket closed. Attempting to reconnect.`);
                this.run(ws);
            })
        })
    }

    public async getLocation() {
        const res = await req(apiUrl)
        .method('POST')
        .body({
          req: "location"
        })
        .json();

        return res.location;
    }

    public async login(ws: WebSocket, location: string) {
        let data = {
            req: "login",
            username: this.username,
            userpass: this.password,
            requestIdx: this.requestIdx,
            location: location
        }
        this.send(ws, data);
        consola.info(`${this.username} | Logging in`);
    }

    public async send(ws: WebSocket, data: any) {
        if (!ws) return;
        try {
            consola.debug(`${this.username} | Sending:`, data['req']);
            ws.send(Buffer.from(JSON.stringify(data)));
            this.requestIdx += 1;
            this.idx += 1;
        }
        catch (err) {
            consola.error(`${this.username} | Error sending`, err);
        }
    }

    public async getLobbies(ws: WebSocket) {
        let data = {
            all: true,
            req: "channels",
            requestIdx: this.requestIdx
        }
        this.send(ws, data);
        consola.info(`${this.username} | Getting lobbies`);       
    }

    public async joinLobbies(ws: WebSocket, channels: any[]) {
        for (let i = 0; i < 3; i++) {
            let channel = channels[i + (this.priority - 1) * 3].name;
            let data = {
                req: 'join',
                channelname: channel,
                idx: this.idx,
                requestIdx: this.requestIdx,
                status: 'available'
            }
            this.send(ws, data);
            consola.debug(`${this.username} | Joining lobby ${channels[i].name}`);
        }
    }

    public async handleCommand(ws: WebSocket, data: any) {
        let cmd = data;
        cmd.chat = cmd.chat.substring(1);
        let r = await handleCommand(data, this.username);
        if (r) {
            r = `${data.username}, ${r}`;
            this.sendChat(ws, r, data.channelname);
        }
    }

    public async sendChat(ws: WebSocket, chat: string, channel: string) {
        let data = {
            channelname: channel,
            chat: chat,
            req: "chat",
            requestIdx: this.requestIdx
        }
        this.send(ws, data);
    }
}

export default User;
