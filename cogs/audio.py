import asyncio
import discord
from discord.ext import commands


class Audio:
    """ Audio shitposting """

    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.is_playing = False
        self.requests = []


    @staticmethod
    def get_voice_channel(ctx):
        """ Attempt to get a voice channel from the given context """

        result = None
        try:
            result = ctx.author.voice.channel
            if not result:
                raise AttributeError
        except AttributeError:
            return None
        return result


    async def connect_voice(self, channel):
        """ Attempts to connect or move to the given channel """

        try:
            self.voice = await channel.connect()
        except discord.ClientException:
            await self.voice.move_to(channel)
            print(f'moved to voice channel: {str(channel)}')
        else:
            print(f'joined voice channel: {str(channel)}')


    async def disconnect_voice(self):
        """ Disconnect from voice """

        if self.voice is None:
            return

        print(f'disconnecting from voice channel: {str(self.voice.channel)}')
        await self.voice.disconnect(force=True)
        self.voice = None


    async def play_request(self, req):
        """ Attempt to play a request """

        await self.connect_voice(req.channel)

        self.is_playing = True

        # TODO play clip
        print(f'TODO play clip "{req.clip}" in channel "{str(req.channel)}"')
        await asyncio.sleep(2)

        # if no more requests, done playing
        try:
            next_request = self.requests[0]
        except:
            self.is_playing = False
            await self.disconnect_voice()
            return

        # remove the request we just pulled
        try:
            self.requests = self.requests[1:]
        except:
            self.requests = []

        # play the request we just pulled
        await self.play_request(next_request)


    @commands.command(hidden=True)
    @commands.guild_only()
    async def summon(self, ctx):
        """ Summon the bot to the user's voice channel """

        new_channel = self.get_voice_channel(ctx)

        if new_channel is None:
            await ctx.send(f"You're not in a voice channel, {ctx.author.mention}.")
            return False

        await self.connect_voice(new_channel)
        return True


    @commands.command(hidden=True)
    @commands.guild_only()
    async def dismiss(self, ctx):
        """ Dismiss the bot from its current voice channel """

        if self.voice is None:
            await ctx.send(f"I'm not in a voice channel, {ctx.author.mention}.")
            return False

        await self.disconnect_voice()
        return True


    @commands.command(hidden=False, brief="Play an audio clip.", enabled=False)
    @commands.guild_only()
    async def play(self, ctx, *, clip: str):
        """ Play an audio clip. You must be in a voice channel. """
        pass


def setup(bot):
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')
    bot.add_cog(Audio(bot))
