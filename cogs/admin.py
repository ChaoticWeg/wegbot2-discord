""" Administrative commands """

import discord
from discord.ext import commands

from .utils import _random

class Admin:
    """ Administrative tasks. Only usable by the owner. """

    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True, name="restart", enabled=False)
    @commands.is_owner()
    async def _restart(self, ctx):
        """ Restart the bot.
            Only usable by the owner. """

        await ctx.send(_random.goodbye())
        # await ctx.bot.restart()


    def reload_extension(self, ext):
        """ Attempt to load an extension. Returns True iff successful, otherwise False """

        try:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)
        except:
            return False
        else:
            return True


    def reload_all(self):
        """ Attempt to reload all extensions """

        starting_count = len(tuple(self.bot.extensions))
        self.bot.logger.info(f'reloading {starting_count} extensions')

        failed = []

        for ext in tuple(self.bot.extensions):
            if not self.reload_extension(ext):
                failed.append(ext)

        if failed:
            self.bot.logger.warning(f'failed to reload extension(s): {", ".join(failed)}')
        else:
            self.bot.logger.info('all extensions reloaded OK')

        return failed


    @commands.command(hidden=True, name="reload")
    @commands.is_owner()
    async def _reload(self, ctx, ext_name='all'):
        """ Reload an extension, or the entire bot.
            Only usable by the owner. """

        await ctx.trigger_typing()

        try:

            # reload all

            if ext_name.lower() == 'all':
                failed = self.reload_all()

                if failed:
                    await ctx.send(f"Failed to reload `{'`, `'.join(failed)}`.")
                else:
                    await ctx.send(f"Reloaded {len(tuple(self.bot.extensions))} extensions.")

                return

            # reload specific

            ext_name = ext_name.lower()
            if not ext_name.startswith('cogs.'):
                ext_name = f"cogs.{ext_name}"

            self.bot.logger.info(f'reloading extension {ext_name}')
            self.bot.unload_extension(ext_name)
            self.bot.load_extension(ext_name)

        except ModuleNotFoundError:
            self.bot.logger.warning(f'unable to reload extension {ext_name}: {ex}')
            await ctx.send(f"No such extension: `{ext_name.replace('cogs.', '')}`")
        except discord.ClientException as ex:
            self.bot.logger.warning(f'failed to reload extension {ext_name}: {ex}')
            await ctx.send(f"I'm having trouble loading `{ext_name}`, {ctx.author.mention}. Check the logs.")
        except Exception as ex:
            self.bot.logger.warning(f'failed to reload extension {ext_name}: {ex}')
            await ctx.send(f"Failed to reload `{ext_name}` - {ex}")
        else:
            self.bot.logger.info(f'successfully reloaded extension {ext_name}')
            await ctx.send(f"Reloaded extension: `{ext_name.replace('cogs.', '')}`")


    @commands.command(hidden=True)
    @commands.is_owner()
    async def bye(self, ctx):
        """ Kill the bot """

        self.bot.logger.critical(f"quit requested by {str(ctx.author)}")
        goodbye = _random.goodbye()
        await ctx.send(goodbye)
        await self.bot.logout()



def setup(bot):
    bot.add_cog(Admin(bot))
