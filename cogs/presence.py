import discord
from discord.ext import commands

class Presence:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def presence(self, ctx, *, new_name: str):
        new_game = discord.Game(name=new_name)
        await self.bot.change_presence()

def setup(bot):
    bot.add_cog(Presence(bot))
