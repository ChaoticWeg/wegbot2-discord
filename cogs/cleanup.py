import os
from discord.ext import commands

class Cleanup:
    """ Cleans up the bot testing channel """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def purge(self, ctx):
        """ Purge the channel """

        if not ctx.author.id == os.getenv('DISCORD_OWNER'):
            await ctx.send(f"You don't have permission to purge this channel, {ctx.author.mention}.")
            return

        if not ctx.channel.id == os.getenv('DISCORD_HOME_CHANNEL'):
            await ctx.send(f"I can't purge this channel, {ctx.author.mention}.")
            return

        await ctx.channel.purge()

def setup(bot):
    bot.add_cog(Cleanup(bot))
