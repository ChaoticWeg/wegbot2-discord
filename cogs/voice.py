from discord.ext import commands

class Voice:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False)
    async def play(self, ctx, *, clip: str):
        print(f'going to play: {clip}')

def setup(bot):
    bot.add_cog(Voice(bot))
