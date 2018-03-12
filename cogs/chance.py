import random
import re

import discord
from discord.ext import commands

class Chance:
    def __init__(self, bot):
        random.seed()
        self.bot = bot
        self.is_valid_re = re.compile('^[1-9]?d[1-9][0-9]*$', flags=re.I)

    def is_valid(self, arg):
        return self.is_valid_re.match(arg)

    @commands.command(hidden=False, brief="Roll the dice.")
    async def roll(self, ctx, dice='1d20'):
        """ Roll an XdY, where
                X = number of dice to roll (optional, default: 1)
                Y = number of sides on each die
            Default roll: 1d20
            Example rolls: 4d8, d6, 2d12

            Coming soon: support for modifiers """

        await ctx.channel.trigger_typing()

        if not self.is_valid(dice):
            await ctx.send(f'"_{dice}_" is not a valid dice roll.')
            return

        parts = dice.lower().split('d')

        count = int(parts[0]) if parts[0] else 1
        sides = int(parts[1])
        total = 0

        index = 0
        while index < count:
            total += random.randint(1, sides)
            index += 1

        description = f'{ctx.author.mention} rolled a **{total}** on **{count}d{sides}**.'
        embedded = discord.Embed(title=f'Roll: {count}d{sides}', description=description)

        await ctx.send(embed=embedded)

def setup(bot):
    bot.add_cog(Chance(bot))
