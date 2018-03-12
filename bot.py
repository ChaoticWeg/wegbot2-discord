import os, sys
from discord.ext import commands

def _prefix_callable(bot, msg):
    user_id = bot.user.id
    result = [ f'<@!{user_id}> ', f'<@{user_id}> ', ';' ]
    return result

EXTENSIONS = {
    'cogs.admin',
    'cogs.audio',
    'cogs.potatoes',
    'cogs.chance',
    'cogs.cleanup'
}

class Wegbot(commands.AutoShardedBot):
    """ Wegbot. Subclass of commands.AutoShardedBot. """

    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, description="Wegbot", owner_id=int(os.getenv('DISCORD_OWNER')))

        self.token = os.getenv('DISCORD_TOKEN')

        for extension in EXTENSIONS:
            try:
                print(f'loading extension {extension:.<15} ', end='')
                self.load_extension(extension)
            except Exception as ex:
                print(f'FAILED: {ex}')
            else:
                print('OK')

    @staticmethod
    def kill(code):
        print(f'killing bot with code: {code}')
        sys.exit(code)

    async def on_ready(self):
        print(f'logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        try:
            await self.process_commands(message)
        except commands.errors.MissingRequiredArgument:
            self.send_message(message.channel, 'Missing a required argument. Use ;help for help.')
        except commands.errors.CommandNotFound as ex:
            self.send_message(message.channel, f"`{ex}`")

    async def on_command_error(self, ctx, error):
        try:
            raise error
        except commands.errors.NotOwner:
            await ctx.send(f"You are not authorized to do that, {ctx.author.mention}.")
        except commands.errors.CommandNotFound:
            await ctx.send(f"No such command, {ctx.author.mention}. Use `;help` for help.")
        except commands.errors.MissingRequiredArgument:
            await ctx.send(f"You're missing an argument there, {ctx.author.mention}. Use `;help` for help.")
        except commands.errors.TooManyArguments:
            await ctx.send(f"Too many arguments there, {ctx.author.mention}. Use `;help` for help.")
        except commands.errors.MissingPermissions:
            await ctx.send(f"You don't have the right permissions in this server to do that, {ctx.author.mention}.")
        except commands.errors.BotMissingPermissions:
            await ctx.send(f"I don't have the right permissions to do that here, {ctx.author.mention}.")
        except commands.errors.NoPrivateMessage:
            await ctx.send(f"You can't use that command in DMs, {ctx.author.mention}.")
        except commands.errors.CommandOnCooldown as ex:
            await ctx.send(f"That command is on cooldown for {ex.retry_after} second(s) longer, {ctx.author.mention}.")
        else:
            print('on_command_error, but no error?')

    def run(self):
        super().run(self.token)
