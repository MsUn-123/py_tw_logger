from twitchio.ext import commands, routines
from datetime import datetime
from enum import Enum

from settings import *
import db
import utils

utility = utils.Utils()
dbWorker = db.DBworker(db_name=CHANNELS[1]) #todo: this is hardcoded thing, change it to dynamic

class LogType(Enum):
    MESSAGE = 0
    TIMEOUT = 1

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix='*', initial_channels=CHANNELS)

    async def event_ready(self):
        print(f'{self.nick} is up and running!')
        self.ping_routine.start()

    #todo: add ebent_timeout
    async def event_message(self, message):
        if message.echo:
            return
        if message.channel.name == CHANNELS[0]:#wtf is this
            return
        
        #todo: see execute() method in db.py - add specification of db name in first parameter
        message_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await dbWorker.log_message({'type': LogType.MESSAGE.value, 'datetime': message_time, 'username': message.author.name, 
                                    'content': message.content, 'raw_data': message.raw_data})
        await self.handle_commands(message)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        '''Manual ping command'''
        if ctx.author.name == DEV_NAME:
            await ctx.send(f'AYAYA <3')

    @routines.routine(hours=1, iterations=0)
    async def ping_routine(self):
        '''Routine to show uptime in it's channel every hour.'''
        await bot.get_channel(CHANNELS[0]).send(f'My uptime: {utility.get_uptime()}')


bot = Bot()
bot.run()