import os

from .audio import Audio
from .clips import Clips
from .clips import setup as setup_clips

def setup(bot):
    setup_clips(bot)
    bot.add_cog(Audio(bot))
