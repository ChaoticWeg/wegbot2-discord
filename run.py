""" Main executing file. Loads .env, creates bot, runs bot """

import logging
logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv  # do we need this? pipenv loads automatically
from bot import Wegbot

def run():
    """ Main executing function """

    load_dotenv()

    bot = Wegbot()
    bot.run()

if __name__ == '__main__':
    run()
