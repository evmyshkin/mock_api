1. `git clone git@github.com:evmyshkin/mouse_api.git`
2. `cd mouse_api`
3. `npm install`
4. `cd src`
7. `sudo ufw allow PORT` where PORT is your desired port
8. `sudo ufw enable`
9. `sudo ufw status`
10. `nano .env`
11. set PORT in .env
12. `pm2 start index.js --name POD_NAME ; pm2 logs POD_NAME --lines 50` where POD_NAME is the desired name for the process
