import WebSocket, { RawData } from 'ws';
import req from '@aero/http';
import important from '../important.json';
import { LocationResponse, WsMessage } from './types'
import consola from 'consola';
import open from 'open';

const apiUrl = new URL('https://web.fightcade.com/api');
const wsUrl = new URL('wss://ggs.fightcade.com/ws/');

//   "JoJo's Bizarre Adventure: Heritage for the Future / JoJo no Kimyou na Bouken: Mirai e no Isan (Japan 990913, NO CD)",
//   "Super Street Fighter II X - grand master challenge (super street fighter 2 X 940223 Japan)",
//   "Street Fighter III 3rd Strike: Fight for the Future (Japan 990512, NO CD)"
const channels = [
  "WCW World Championship Wrestling (USA) (NES)",
];

let wsHeader = {
  'User-Agent': 'Fightcade2-WIN32-v2.1.26',
}

let location = '';
let ws: WebSocket | undefined;
let requestIdx = -1;
let idx = 0;

async function send(data: any) {
  if (ws) {
    try {
      consola.debug('Sending:', data);
      ws.send(Buffer.from(JSON.stringify(data)));
      requestIdx++;
      idx++;
    } catch (e) {
      consola.error('Error sending:', e);
    }
  }
}

async function getLocation() {
  const res: LocationResponse = await req(apiUrl)
    .method('POST')
    .body({
      req: "location"
    })
    .json();

  return res.location;
}

async function login(location: string) {
  const { username, userpass } = important;
  let data = {
    req: "login",
    username,
    userpass,
    requestIdx,
    location,
  }
  send(data);
}

async function joinLobby(channel: string) {
  let data = {
    'away': 'false',
    'channelname': channel,
    'idx': idx,
    'req': 'join',
    'requestIdx': requestIdx,
    'status': 'available'
  }
  send(data);
}

async function joinLobbies() {
  for (let channel of channels) {
    consola.info('Joining lobby:', channel)
    await joinLobby(channel);
  }
}

async function run(): Promise<void> {
  return new Promise(async (resolve, reject) => {
    location = await getLocation();

    consola.success('Got location');

    ws = new WebSocket(wsUrl, {
      headers: wsHeader,
      origin: "https://web.fightcade.com",
      host: "ggs.fightcade.com"
    });

    ws.on('open', connected);

    ws.on('error', (err) => {
      consola.error('Websocket error', err);
    });

    ws.on('message', handleMessage);

    ws.on('close', () => {
      consola.error('Websocket closed');
      resolve();
    })
  })
}

async function connected() {
  consola.debug('Websocket connected');

  await login(location);
}

async function handleMessage(msg: RawData) {
  const data = JSON.parse(msg.toString('utf8')) as WsMessage;
  consola.debug('Websocket message:', data.req);

  if (data.req === 'login') {
      await handleLogin(data);
      consola.info('Recieved token:', data['user']['token']);
      
      let uri = 'fcade://userstatus/stwlan/' + data['user']['token']; 
    
      open(uri);
      consola.info('Opening:', uri);
  }

  if (data.req === 'join' && data.result === 200) {
    consola.success('Joined lobby:', data.channelname);
  }

  consola.debug("WS DATA:", data);

  if (data.req === 'chat') {
    if (data.result) return;
    consola.info(data.username + ':', data.chat, ' | ', data.channelname);

    if (data.chat.startsWith('!rom')) {
      let msg = '@{}, ROMs can be found at https://krypton.sh/'.replace('{}', data.username);
      sendChat(data.channelname, msg);
    }
  }
  
  if (data.req === 'updateuser') {
      consola.info('updateuser')
  }
}

async function handleLogin(data: any) {
  if (data.result === 200) {
    consola.success('Logged in as ' + data.username);

    await joinLobbies();
  }
}

async function sendChat(channel: string, message: string) {
  let chatData = {
    'channelname': channel,
    'chat': message,
    'req': 'chat',
    'requestIdx': requestIdx,
  }
  send(chatData)
}

run().then(() => {
  consola.info('done');
}).catch(e => {
  consola.info(e);
});