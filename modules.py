from twitchio.ext.commands import Cog

class Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_user_timeout(self, channel, user, duration, reason):
        await channel.send(f"{user} has been timed out for {duration} seconds. Reason: {reason}")

def setup(bot):
    bot.add_cog(Listeners(bot))