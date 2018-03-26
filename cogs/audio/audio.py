import discord
from discord.ext import commands

from cogs.errors import WegbotException
from .clips import get_by_name as get_clip


class AudioRequest:
    """ Audio request """
    def __init__(self, channel, clip, msg):
        self.channel = channel
        self.clip = clip
        self.msg = msg


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
            self.bot.logger.info(f'moved to voice channel: {str(channel)}')
        else:
            self.bot.logger.info(f'joined voice channel: {str(channel)}')


    async def disconnect_voice(self):
        """ Disconnect from voice """

        if self.voice is None:
            return

        self.bot.logger.info(f'disconnecting from voice channel: {str(self.voice.channel)}')
        await self.voice.disconnect(force=True)
        self.voice = None


    @commands.command(hidden=True, name='requests')
    @commands.guild_only()
    async def say_requests(self, ctx):
        """ Shows queued requests """
        if not self.requests:
            await ctx.send(f"No requests, {ctx.author.mention}! Queue one up with `;play`.")
            return
        await ctx.send(f"{ctx.author.mention} – I have {len(self.requests)} queued up right now!")


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


    async def force_dismiss(self, ctx):
        if ctx.voice_client is None:
            raise WegbotException("Unable to force dismiss: no voice client")
        await ctx.voice_client.disconnect()


    @commands.command(hidden=True)
    @commands.guild_only()
    async def dismiss(self, ctx):
        """ Dismiss the bot from its current voice channel """

        if self.voice is None:
            try:
                await self.force_dismiss(ctx)
            except WegbotException:
                await ctx.send(f"I'm not in a voice channel, {ctx.author.mention}.")
                return False
            else:
                return True
        else:
            await self.disconnect_voice()
            return True


    @commands.command(hidden=False, brief="Play an audio clip.")
    @commands.guild_only()
    async def play(self, ctx, *, clip_name: str):
        """ Play an audio clip. You must be in a voice channel. """
        try:

            clip = get_clip(clip_name)
            if clip is None:
                raise WegbotException(f"I don't know any clips called '{clip_name}'")

            # TODO add clip to queue
            # maybe have another loop playing from the queue
            # anyway here's an exception
            raise WegbotException("I can't play clips yet")

        except WegbotException as ex:
            await ctx.send(f"{ex.message}, {ctx.author.mention}.")
            return False

# --> setup() is in __init__.py
