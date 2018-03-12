import random

IS_SEEDED = False

GOODBYES = [
    'Later!',
    'Peace.',
    'afk',
    'afk, tornado',
    'brb server on fire',
    'brb cat on fire',
    '`ACKNOWLEDGEMENT AND ACCEPTANCE OF TERMS`',
    '```\n*** ChaoticWeg sets mode: +b wegbot*!*@*.*\nwegbot has been kicked by ChaoticWeg ( )\n```',
    'YOU ALL SUCK DICK\ner.\nbye.',
    "/me is away - gone, if anyone talks in the next 25 minutes as me it's weg being an asshole -",
    'IRC is just multiplayer notepad.',
    'wait, shit',
    'yaYEEEET',
    'Adiós.',
    'Au revoir!',
    'Shutting down...',
    'Whoops',
    "fuck you i didn't touch the cookie, bitch",
    '/me has quit IRC (r`heaven)',
    '/me takes a bow',
    '/me is now known as wegbotWITHGIRLFRIENDWHOISHOT',
    'dammit',
    "Ok I'm back.",
    "`*** Quits: wegbot (No route to host)`",
    "`wegbot has quit IRC. (Quit)`"
]

def _check_seed():
    global IS_SEEDED
    if not IS_SEEDED:
        random.seed()

def goodbye():
    global GOODBYES
    idx = random.randint(0, len(GOODBYES)-1)
    return GOODBYES[idx]
