from discord.ext import commands

class Admin:
    """ Administrative tasks. Only usable by the owner.
        Notes:
            - Use ;reload to load an extension for the first time. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, name="restart", enabled=False)
    @commands.is_owner()
    async def _restart(self, ctx):
        """ Restart the bot.
            Only usable by the owner. """

        await ctx.send("brb")
        # await ctx.bot.restart()

    def reload_extension(self, ext):
        try:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)
        except:
            return False
        else:
            return True

    @commands.command(hidden=True, name="reload")
    @commands.is_owner()
    async def _reload(self, ctx, ext_name: str):
        """ Reload an extension, or the entire bot.
            Only usable by the owner. """

        await ctx.trigger_typing()

        try:

            # reload all

            if ext_name.lower() == 'all':
                failed = []

                for ext in tuple(self.bot.extensions):
                    if not self.reload_extension(ext):
                        print(f'failed to reload extension: {ext}')
                        failed.append(ext)

                if failed:
                    await ctx.send(f"Failed to reload extension(s): {','.join(failed)}.")
                else:
                    await ctx.send(f"Successfully reloaded {len(tuple(self.bot.extensions))} extensions.")

                return

            # reload specific

            ext_name = ext_name.lower()
            if not ext_name.startswith('cogs.'):
                ext_name = f"cogs.{ext_name}"

            print(f'reloading extension {ext_name:.<15}... ', end='')
            self.bot.unload_extension(ext_name)
            self.bot.load_extension(ext_name)
        except ModuleNotFoundError:
            print('NOT FOUND')
            await ctx.send(f"No such extension: `{ext_name.replace('cogs.', '')}`")
        except Exception as ex:
            print(f'FAILED: {ex}')
            await ctx.send(f"Failed to reload `{ext_name}`: {ex}")
        else:
            print('OK')
            await ctx.send(f"Reloaded extension: `{ext_name.replace('cogs.', '')}`")

def setup(bot):
    bot.add_cog(Admin(bot))
