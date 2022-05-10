import consola from 'consola';
import important from '../important.json';
import User from './User';

let priority = 0;
for (let account in important.accounts) {
    priority++;
    let user = new User(important.accounts[account].username, important.accounts[account].userpass, 0, 0, priority);
    consola.success(`${user.username} | Created user`);
}
