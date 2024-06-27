1. `git clone git@github.com:evmyshkin/mouse_api.git`
2. `cd mouse_api`
3. `npm install`
7. `sudo ufw allow PORT` where PORT is your desired port
8. `sudo ufw enable`
9. `sudo ufw status`
10. `nano .env`
11. set PORT in .env
12. `pm2 start index.js --name POD_NAME ; pm2 logs POD_NAME --lines 50` where POD_NAME is the desired name for the process

![image](https://github.com/evmyshkin/mouse_api/assets/74656967/4b51fe6b-41b4-4767-80f5-391d18ce6ae0)
