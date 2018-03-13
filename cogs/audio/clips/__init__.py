from .registry import Registry as Clips

def setup(bot):
    Clips.load_all()
