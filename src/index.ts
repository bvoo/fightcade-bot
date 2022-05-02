import WebSocket, { RawData } from 'ws';
import req from '@aero/http';
import important from '../important.json';
import { LocationResponse, WsMessage } from './types'
import consola from 'consola';

const apiUrl = new URL('https://web.fightcade.com/api');
const wsUrl = new URL('wss://ggs.fightcade.com/ws/');

const channels = [
  "JoJo's Bizarre Adventure: Heritage for the Future / JoJo no Kimyou na Bouken: Mirai e no Isan (Japan 990913, NO CD)",
  "Super Street Fighter II X - grand master challenge (super street fighter 2 X 940223 Japan)",
  "Street Fighter III 3rd Strike: Fight for the Future (Japan 990512, NO CD)"
];

let wsHeader = {
  'User-Agent': important.fightcade_version
}

let location = '';
let ws: WebSocket | undefined;
let requestIdx = 0;
let idx = 0;

async function send(data: any) {
  if (ws) {
    try {
      ws.send(JSON.stringify(data));
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
  }

  if (data.req === 'join' && data.result === 200) {
    consola.success('Joined lobby:', data.channelname);
  }

  if (data.req === 'chat' && data.username != important.username) {
    consola.info(data.username + ':', data.chat, ' | ', data.channelname);
    if (data.chat.toLowerCase().includes('rom')) {
      xqcS(data.channelname);
    }
  }
}

async function handleLogin(data: any) {
  if (data.result === 200) {
    consola.success('Logged in as ' + data.username);

    await joinLobbies();
  }
}

async function xqcS(channel: string) {
  // do that
}

run().then(() => {
  consola.info('done');
}).catch(e => {
  consola.info(e);
});