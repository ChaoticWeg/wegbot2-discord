import os

from .audio import Audio
from .clips import Clips
from .clips import setup as setup_clips

def load_ffmpeg():
    previous_path = os.getenv('PATH')
    ffmpeg_path = os.getenv('FFMPEG_PATH', default='')
    os.environ['PATH'] = previous_path + ':' + ffmpeg_path

def setup(bot):
    load_ffmpeg()
    setup_clips(bot)
    bot.add_cog(Audio(bot))
