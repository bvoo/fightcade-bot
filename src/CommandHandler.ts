import consola from 'consola';

async function handleCommand(command: any, username: string) {
    let cmd = command.chat.split(' ')[0];
    let args = command.chat.split(' ').slice(1);

    if (args) {
        consola.info(`${username} | User: ${command.username} | Command: ${cmd} | Args: ${args}`);
    }
    else {
        consola.info(`${username} | User: ${command.username} | Command: ${cmd}`);
    }

    switch (cmd) {
        case 'morbius':
            return '#MorbiusSweep https://tenor.com/view/morbius-morbius-sweep-gif-25378327 https://cdn.discordapp.com/attachments/950667635723477042/970896014846341171/morbius.mp4';
        default:
            return 'Unknown command';
    }
}

export default handleCommand;
