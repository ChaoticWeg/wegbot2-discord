""" Combines the commands in this directory into one cog """

class Messaging:
    """ Message-related commands """

    def __init__(self, bot):
        self.bot = bot

    from .pin import pin_that
    from .purge import purge
    from .nuisance import nuisance


def setup(bot):
    bot.add_cog(Messaging(bot))
