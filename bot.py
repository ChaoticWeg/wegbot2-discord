""" The actual, real dang bot """

import os
import discord
from discord.ext import commands

from cogs.errors import WegbotException

def _prefix_callable(bot, msg):
    """ Returns a list of valid command prefixes """
    user_id = bot.user.id
    result = [ f'<@!{user_id}> ', f'<@{user_id}> ', ';', '?' ]
    return result

# extensions to be loaded at runtime
EXTENSIONS = {
    'cogs.admin',
    'cogs.audio',
    'cogs.potatoes',
    'cogs.chance',
    'cogs.messaging'
}

### WEGBOT WEGBOT WEGBOT

class Wegbot(commands.AutoShardedBot):
    """ Wegbot. Subclass of commands.AutoShardedBot """

    def __init__(self):
        """ Constructor """
        super().__init__(command_prefix=_prefix_callable, description="Wegbot", owner_id=int(os.getenv('DISCORD_OWNER')))

        self.token = os.getenv('DISCORD_TOKEN')

        for extension in EXTENSIONS:
            try:
                print(f'loading extension {extension:.<18} ', end='')
                self.load_extension(extension)
            except Exception as ex:
                print(f'FAILED: {ex}')
            else:
                print('OK')


    async def set_presence(self):
        """ Set presence according to environment """

        try:

            game = None
            status = discord.Status.online

            disc_env = os.getenv('DISCORD_ENVIRONMENT')
            if disc_env.lower() == 'production':
                game = discord.Game(name=f"Wegbot v{os.getenv('WEGBOT_VERSION')} – ?help")
            elif disc_env.lower() == 'development':
                game = discord.Game(name="(in development)")
                status = discord.Status.dnd
            else:
                game = discord.Game(name=disc_env)

            await self.change_presence(activity=game, status=status)

        except Exception as ex:
            print(f"Unable to set presence! {ex}")
        else:
            print("successfully set presence")


    async def on_connect(self):
        """ What to do when the bot connects (not ready yet though) """

        print('connected to discord')
        await self.set_presence()


    async def on_ready(self):
        """ What to do when the bot is ready for action """

        print(f'logged in as {self.user}')


    async def on_message(self, message):
        """ What to do when we see a new message """

        if message.author.bot:
            return

        await self.process_commands(message)


    async def on_command_error(self, ctx, error):
        """ What to do when a command raises an unexpected error """
        # this shit is fuckin trash dawg

        try:
            raise error
        except WegbotException as ex:
            await ctx.send(f"{ex.message}, {ctx.author.mention}")
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
            await ctx.send(f"You can't use that command in DMs.")
        except commands.errors.CommandOnCooldown as ex:
            await ctx.send(f"That command is on cooldown for {ex.retry_after} second(s) longer, {ctx.author.mention}.")
        except commands.errors.DisabledCommand:
            await ctx.send(f"Sorry {ctx.author.mention}, that command is disabled for now.")
        except commands.errors.BadArgument as ex:
            await ctx.send(f"{ex}. Use `;help` for help.")
        else:
            print('on_command_error, but no error?')


    def run(self):
        """ Remove the need for a token, since it's retrieved automagically from .env """

        super().run(self.token)
