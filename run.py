from dotenv import load_dotenv
load_dotenv()

import discord
import asyncio
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {} ({})'.format(client.user.name, client.user.id))

@client.event
async def on_message(message):
    print('message')

client.run(os.getenv('DISCORD_TOKEN'))