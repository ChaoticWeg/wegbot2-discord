""" Info commands """

import discord
from discord.ext import commands

class Info:
    """ Wegbot information """

    def __init__(self, bot):
        self.bot = bot
        self.github_repo = "ChaoticWeg/wegbot2-discord"


    @property
    def github_url(self):
        return f"https://github.com/{self.github_repo}"


    @commands.group(name='info', invoke_without_command=True, hidden=True)
    async def _info(self, ctx):
        """ Bot info. """

        embedded = discord.Embed()\
                        .add_field(name="Version", value=self.bot.version)\
                        .add_field(name="Github Repo", value=self.github_url)

        await ctx.send(f"Here's my info, {ctx.author.mention}.", embed=embedded)


    @_info.command(hidden=False)
    async def version(self, ctx):
        """ Bot version info. """

        await ctx.send(f"{ctx.author.mention} – Wegbot {self.bot.version}, in {self.bot.environment}")


    @_info.command(hidden=False)
    async def github(self, ctx):
        """ Github repo info. """

        embedded = discord.Embed(title=self.github_repo, url=self.github_url,
                                 description="View Wegbot source on GitHub.", author="ChaoticWeg")

        await ctx.send(f"Here's a link to my GitHub repo, {ctx.author.mention}.", embed=embedded)


    @commands.command(hidden=False, name='version')
    async def _version(self, ctx):
        """ Bot version info. """
        await ctx.invoke(self.version)
    

    @commands.command(hidden=False, name='github')
    async def _github(self, ctx):
        """ Github repo info. """
        await ctx.invoke(self.github)



def setup(bot):
    bot.add_cog(Info(bot))
