import os
import discord

from .audio import Audio
from .clips import Clips
from .clips import setup as setup_clips

def load_opus():
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')

def setup(bot):
    load_opus()
    setup_clips(bot)
    bot.add_cog(Audio(bot))
