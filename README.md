# Twtich-chat message logger

## About <a name = "about"></a>

Simple bot that can log messages from a twitch channel to a database of the said channel. This database, for example, can be accessed by everyone using web page.

## Getting Started <a name = "getting_started"></a>

This bot uses python3.9

*something about git clone...*
```
git clone https://github.com/MsUn-123/tw_logger
cd tw_logger
```

*something about virtual environment and requirements...*
```
virtualenv .venv
source .venv/bin/activate
pip install -r requeirments.txt
```

## Installing and usage

Create `settings.py` file with variables:

Please notice that first channel in CHANNELS should be your bot channel name. (TODO: rework this)
```
ACCESS_TOKEN = <your bots' API key>
BOT_NAME = <your bots name>
DEV_NAME = <your twitch nickname, it's used to access bots commands>
CHANNELS = <channel chats to log>
```

Before starting a bot run `db.py` to create database for every channel.
```
python db.py
```


To start logging use: 
```
python bot.py
```
## Commands

*stats - show stats of the channel (using your database of this channel)

*ping - Pong! Uptime: *h:m*. RAM used: *%*.

## TO-DO
general:
- [ ] Create minimal web project to interact with databases.
- [ ] Change installation method.
- [ ] Move files to corresponding folders.
- [x] Add prefix to settings.py

perfomance:
- [ ] Use batches of messages to improve perfomance. (if logging big amount of messages it can throw random errors)
- [ ] Make pool of connections. Investigate if we really need this.

bot.py:
- [x] Make auto ping routine not dependable on CHANNELS variable.
- [x] Make db connection dynamic instead of hardcoded CHANNELS[1] (logs only one channel). Change log_message method.
- [ ] Add timeout_event and log it as LogType.TIMEOUT.value with raw_data empty.
- [x] Add stats command.
- [ ] Rework get_stats method. Make it more beautiful.
- [ ] Invoke stats command on stream end.
- [ ] ~~Rework *ping command: *ping - "Pong! Uptime - <time>, temp - <c°>, ram - <mb> + %.~~ See utils.py section.
- [ ] Rework *stats command to get stats of any tracked channel: *stats <channel>.
- [x] Remove ping routine
- [ ] On stream end form stats report and document it using stats.py (or/and show in chat (make it optional)).

db.py:
- [ ] Overhaul databases initiation and check if db exist for CHANNEL, create one if there is none.
- [ ] Add get_data method for stats command.
- [ ] Add emoji support.
- [ ] Split db.py into logger.py and stats.py

stats.py:
- [ ] Create stats.py - this class will get random statistics from sqlite databases. 
- [ ] Also make this class working with json channel files.

utils.py:
- [x] Fix get_uptime method
- [x] Add platform stats - RAM usage (%).
- [ ] Add platform stats - temp.

modules.py:
- [ ] Move events to modules file and add more event handlers.


## Contributing <a name = "contributing"></a>

Feel free to contribute! Any help is appreciated and it will help me to learn new things!
