from dotenv import load_dotenv
from bot import Wegbot

def run():
    load_dotenv()

    bot = Wegbot()
    bot.run()

if __name__ == '__main__':
    run()
