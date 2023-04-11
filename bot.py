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
                         prefix='*', 
                         initial_channels=CHANNELS)

    async def event_ready(self):
        print(f'{self.nick} is up and running!')
        await self.join_self(f'{self.nick}')

    async def join_self(self, channel_name):
        await bot.join_channels([channel_name])
        self.ping_routine.start()
        
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
        '''Manual ping command'''
        if ctx.author.name == DEV_NAME:
            print(self.connected_channels[-1].name)
            await ctx.send(f'pong!')
    
    @commands.command()
    async def stats(self, ctx: commands.Context):
        '''Some stats for channel'''
        if ctx.author.name == DEV_NAME:
            await ctx.send(f'{await dbWorker.get_stats(_channel=ctx.channel.name)}')


    @routines.routine(minutes=30, iterations=0)
    async def ping_routine(self):
        '''Routine to show uptime in it's channel every hour.\n
           This method will break if you add manual channel join command.\n
           Also this routine skips first iteration because bot needs time to connect to its channel.'''
        await bot.get_channel(self.connected_channels[-1].name).send(f'My uptime: {utility.get_uptime()}')


bot = Bot()
bot.run()