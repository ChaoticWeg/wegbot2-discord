import asyncio
import discord
from discord.ext import commands


class AudioRequest:
    """ Audio request """

    def __init__(self, channel, clip):
        self.channel = channel
        self.clip = clip



class AudioPlayer:
    """ Audio player """

    def __init__(self):
        pass



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
        await self.connect_voice(req.channel)

        self.is_playing = True

        # TODO play clip
        print(f'TODO play clip "{req.clip}" in channel "{str(req.channel)}"')
        await asyncio.sleep(2)

        if not self.requests:
            self.is_playing = False
            await self.disconnect_voice()
            return

        next_request = self.requests[0]

        try:
            self.requests = self.requests[1:]
        except:
            self.requests = []

        await self.play_request(next_request)


    @commands.command(hidden=True)
    async def summon(self, ctx):
        """ Summon the bot to the user's voice channel """

        # will be User if in DM -- User does not have VoiceStatus
        if isinstance(ctx.author, discord.User):
            await ctx.send("I can't be summoned via DM.")
            return False

        new_channel = self.get_voice_channel(ctx)
        if new_channel is None:
            await ctx.send(f"You're not in a voice channel, {ctx.author.mention}.")
            return False

        await self.connect_voice(new_channel)
        return True

    @commands.command(hidden=True)
    async def dismiss(self, ctx):
        """ Dismiss the bot from its current voice channel """

        if self.voice is None:
            end = f", {ctx.author.mention}" if isinstance(ctx.channel, discord.TextChannel) else ""
            await ctx.send(f"I'm not in a voice channel{end}.")
            return False

        await self.disconnect_voice()
        return True

    @commands.command(hidden=False)
    async def play(self, ctx, *, clip: str):
        requested_channel = self.get_voice_channel(ctx)
        if requested_channel is None:
            await ctx.send(f"You're not in a voice channel, {ctx.author.mention}.")
            return False

        request = AudioRequest(requested_channel, clip)

        if self.is_playing:
            self.requests.append(request)
            print(f"Queued: '{clip}' (in channel: '{str(requested_channel)}')")
            return True

        await self.play_request(request)
        return True


def setup(bot):
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')
    bot.add_cog(Audio(bot))
