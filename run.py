import signal

from dotenv import load_dotenv
from bot import Wegbot

async def handle_sigint(bot):
    await bot.logout()

def run():
    load_dotenv()

    bot = Wegbot()

    # capture sigint
    signal.signal(signal.SIGINT, lambda signal, frame: handle_sigint(bot))

    bot.run()

if __name__ == '__main__':
    run()
