import os
import discord

from dotenv import load_dotenv

def run():
    load_dotenv()

    client = discord.Client()

    @client.event
    async def on_ready():
        print('connected as {}'.format(client.user.name))

    @client.event
    async def on_message(message):
        print('message in {}'.format(str(message.channel)))

        if message.content.startswith(';dump'):
            args = message.split(' ')[1:]
            if not args:
                print('no args to ;dump')
            else:
                print(';dump {}'.format(args[0]))

    client.run(os.getenv('DISCORD_TOKEN'))
