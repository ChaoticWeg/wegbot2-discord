from .registry import Registry as Clips

def setup(bot):
    Clips.load_all()

def get_by_name(name):
    return Clips.get_by_name(name)
