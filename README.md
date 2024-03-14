# Overview
You have one server, which scales with the number of clients \
The client will all share the game state by connecting to the server

## Install
[Step 0] Install repositoy ```git clone https://github.com/AlfSelen/distributedSystem```\
[Step 1] Both for client and server ```pip -r requirements.txt```

## Run
[Step 1] Start server ```python server.py```\
[Step 2] Start any ammount of clients ```python client.py```

## Server.py
  -h, --help       show this help message and exit \
  --server SERVER  IP of server e.g. 127.0.0.1 \
  --port PORT      IP of server e.g. 5555 

## Client.py
  -h, --help       show this help message and exit\
  --game GAME      Given number or name of game to skip initial input, e.g. 0, 1, Box or Ping\
  --server SERVER  IP of server e.g. 127.0.0.1\
  --port PORT      IP of server e.g. 5555

## Configuration
Various setting can be configured
### 

## Inspired by
Python Online Game Tutorial over at https://www.youtube.com/@TechWithTim
