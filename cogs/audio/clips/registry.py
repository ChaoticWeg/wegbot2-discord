import copy
from os import listdir
from os.path import isfile, join, dirname, realpath, splitext

class Clip:
    def __init__(self, name, path):
        self.name = name
        self.path = path
    def __str__(self):
        return self.name

class Registry:
    __inner__ = []

    @staticmethod
    def load_all():
        audio_dir = dirname(realpath(__file__))

        Registry.__inner__ = []
        for filename in listdir(audio_dir):

            if not isfile(join(audio_dir, filename)) or not filename.endswith('.mp3'):
                continue

            name = splitext(filename)[0]
            path = join(audio_dir, filename)

            Registry.__inner__.append(Clip(name, path))

        print(f"{len(Registry.inner())} clip(s), ", end='')

    @staticmethod
    def inner():
        return list(copy.deepcopy(Registry.__inner__))

    @staticmethod
    def get_by_name(name):
        try:
            results = [ clip for clip in Registry.inner() if clip.name.lower() == name ]
            return results[0]
        except:
            return None
