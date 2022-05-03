export type LocationResponse = {
  location: string;
}

export type WsMessage = Chat | Join | Login | UpdateUser;

export type Join = {
  req: 'join';
  result: number;
  channelname: string;
}

export type Login = {
  req: 'login';
  user: {
    username: string;
    token: string;
  }
}

export type Chat = {
  req: 'chat';
  chat: string;
  username: string;
  channelname: string;
  result?: number;
}

export type UpdateUser = {
    req: 'updateuser';
    user: {
        token: string;
    }
}