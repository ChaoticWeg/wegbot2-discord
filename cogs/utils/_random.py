""" Randomized stuff """

import random
random.seed()

GOODBYES = [
    'afk',
    'afk, tornado',
    'brb server on fire',
    '`ACKNOWLEDGEMENT AND ACCEPTANCE OF TERMS`',
    '```\n*** ChaoticWeg sets mode: +b wegbot*!*@*.*\nwegbot has been kicked by ChaoticWeg ( )\n```',
    'YOU ALL SUCK DICK\ner.\nbye.',
    "`*** wegbot is away - gone, if anyone talks in the next 25 minutes as me it's weg being an asshole -`",
    'wait, shit',
    "fuck you i didn't touch the cookie, bitch",
    '`*** wegbot has quit IRC (r`heaven)`',
    '`*** wegbot is now known as wegbotWITHGIRLFRIENDWHOISHOT`',
    'dammit',
    "Ok I'm back.",
    "`*** Quits: wegbot (No route to host)`",
]


def goodbye():
    """ Get a random goodbye """

    # pylint: disable=W0603
    # shut the FUCK UP ABOUT IT
    global GOODBYES
    idx = random.randint(0, len(GOODBYES)-1)
    return GOODBYES[idx]
