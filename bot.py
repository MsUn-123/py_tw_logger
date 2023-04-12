import twitchio
from twitchio.ext import commands, routines
from datetime import datetime
from enum import Enum

from db import DBworker
from utils import Utils
from settings import *

utility = Utils()
dbWorker = DBworker()

class LogType(Enum):
    MESSAGE = 0
    TIMEOUT = 1

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=ACCESS_TOKEN,
                         nickname=BOT_NAME, 
                         prefix=PREFIX, 
                         initial_channels=CHANNELS)

    async def event_ready(self):
        print(f'{self.nick} is up and running!')
        
    #todo: add event_timeout
    async def event_message(self, message):
        if message.echo:
            return

        #todo: see execute() method in db.py - add specification of db name in first parameter
        message_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await dbWorker.log_message(_channel=message.channel.name,
                                   _data_dict={'type': LogType.MESSAGE.value, 'datetime': message_time, 
                                              'username': message.author.name, 'content': message.content, 
                                              'raw_data': message.raw_data})
        await self.handle_commands(message)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        '''Ping command'''
        if ctx.author.name == DEV_NAME:
            await ctx.send(f'Pong! {utility.get_all_stats}')
    
    @commands.command()
    async def stats(self, ctx: commands.Context):
        '''Some stats for channel'''
        if ctx.author.name == DEV_NAME:
            await ctx.send(f'{await dbWorker.get_stats(_channel=ctx.channel.name)}')


bot = Bot()
bot.run()