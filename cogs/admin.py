from discord.ext import commands

class Admin:
    """ Administrative tasks """

    @commands.command(hidden=True, name="restart", disabled=True)
    @commands.is_owner()
    async def _restart(self, ctx):
        """ Restart the bot. Only usable by the owner. """
        await ctx.send("brb")
        # await ctx.bot.restart()

    @commands.command(hidden=True, name="reload")
    @commands.is_owner()
    async def _reload(self, ctx, ext_name: str):
        """ Reload an extension, or the entire bot. Only usable by the owner. """
        await ctx.trigger_typing()

        if not ext_name.startswith('cogs.'):
            ext_name = f"cogs.{ext_name}"

        try:
            print(f'reloading extension {ext_name:.<15}... ', end='')
            ctx.bot.unload_extension(ext_name)
            ctx.bot.load_extension(ext_name)
        except ModuleNotFoundError:
            print('NOT FOUND')
            await ctx.send(f"No such extension: `{ext_name.replace('cogs.', '')}`")
        except Exception as ex:
            print('FAILED')
            print(ex)
            await ctx.send(f"Failed to reload `{ext_name}`: {ex}")
        else:
            print('OK')
            await ctx.send(f"Reloaded extension: `{ext_name.replace('cogs.', '')}`")

def setup(bot):
    bot.add_cog(Admin())
