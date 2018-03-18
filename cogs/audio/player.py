from .request import AudioRequest

class AudioPlayer:

    def __init__(self):
        self._queue = []

    def queue(self, request: AudioRequest):
        self._queue.append(request)
