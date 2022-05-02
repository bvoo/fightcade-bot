export type LocationResponse = {
  location: string;
}

export type WsMessage = Chat | Join | Login;

export type Join = {
  req: 'join';
  result: number;
  channelname: string;
}

export type Login = {
  req: 'login';
}

export type Chat = {
  req: 'chat';
  chat: string;
  username: string;
  channelname: string;
}