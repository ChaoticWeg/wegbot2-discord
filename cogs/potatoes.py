import random
from discord.ext import commands

def make_taters(line_length=20, num_lines=10, taters_per_line=5):
    """ get em while they're hot """
    lines = [ ' ' * line_length for i in range(num_lines) ]

    line_i = 0
    while line_i < num_lines:
        lines[line_i] = ' ' * line_length

        taters_i = 0
        while taters_i < taters_per_line:

            start_pos = random.randint(0, line_length - 1)
            end_pos = start_pos + len("potatoes")

            if end_pos >= len(lines[line_i]):
                end_pos = end_pos - (end_pos - line_length + 1)

            lines[line_i] = lines[line_i][0:start_pos] + "potatoes" + lines[line_i][end_pos:]
            taters_i += 1

        line_i += 1

    result = '\n'.join(lines)
    return f'```\n{result}\n```'


class Taters:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False)
    async def taters(self, ctx):
        """ Generate potato. """
        await ctx.channel.trigger_typing()
        taters = make_taters()
        await ctx.send(taters)


def setup(bot):
    random.seed(None)
    bot.add_cog(Taters(bot))
