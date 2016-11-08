Sistem informasi Indonesia Jamu-Herbs (SI-IJAH) v2

https://nodejs.org/dist/v6.6.0/node-v6.6.0-linux-x64.tar.xz

// install install nodejs
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs

// angular2 webpack :https://github.com/AngularClass/angular2-webpack-starter
sudo npm install webpack-dev-server rimraf webpack -g

// clone git ijah
git clone ...

// install ijah dependencies
cd ijah/
npm install

// run ijah on port 3000
npm run server:dev
