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

        # will be User if in DM; User does not have VoiceStatus
        if isinstance(ctx.author, discord.User):
            await ctx.send(f"I can't be summoned via DM.")
            return

        # no VoiceStatus if not in voice
        try:
            new_channel = ctx.author.voice.channel
            # just force an exception if there's a VoiceStatus with a None channel
            if not new_channel:
                raise AttributeError
        except AttributeError:
            await ctx.send(f"You're not in a voice channel, {ctx.author.mention}.")
            return

        await ctx.send(f"I'll be able to join **{str(new_channel)}** shortly, {ctx.author.mention}.")

def setup(bot):
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')
    bot.add_cog(Audio(bot))
