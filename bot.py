import os
from discord.ext import commands

def _prefix_callable(bot, msg):
    user_id = bot.user.id
    result = [ f'<@!{user_id}> ', f'<@{user_id}> ', ';' ]
    return result

EXTENSIONS = {
    'cogs.audio',
    'cogs.potatoes',
    'cogs.chance',
    'cogs.cleanup'
}

class Wegbot(commands.AutoShardedBot):
    
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, description="Wegbot")

        self.token = os.getenv('DISCORD_TOKEN')

        for extension in EXTENSIONS:
            try:
                print(f'loading extension {extension}... ', end='')
                self.load_extension(extension)
            except Exception as ex:
                print(f'FAILED: {ex}')
            else:
                print('OK')

    async def on_ready(self):
        print(f'logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        try:
            await self.process_commands(message)
        except commands.errors.MissingRequiredArgument:
            self.send_message(message.channel, 'Missing a required argument. Use ;help for help.')

    def run(self):
        super().run(self.token)
