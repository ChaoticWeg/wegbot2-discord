import discord
from discord.ext import commands

class AudioEntry:
    def __init__(self, message):
        self.requester = message.author
        self.channel = message.channel

class AudioState:
    def __init__(self):
        pass

class Audio:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False)
    async def summon(self, ctx):
        new_channel = ctx.message.author.voice_channel
        if not new_channel:
            self.bot.send_message(ctx.message.author, "You're not in a voice channel.")

def setup(bot):
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')
    bot.add_cog(Audio(bot))
