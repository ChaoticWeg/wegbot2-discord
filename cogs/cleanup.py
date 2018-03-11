from discord.ext import commands

class Cleanup:
    """ Cleans up the bot testing channel """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def purge(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Cleanup(bot))
