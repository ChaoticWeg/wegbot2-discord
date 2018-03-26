import random
import re

import discord
from discord.ext import commands

from .errors import WegbotException

class Chance:
    """ Roll dice, flip a coin, etc """

    def __init__(self, bot):
        random.seed()
        self.bot = bot
        self.is_valid_dice_re = re.compile('^[1-9]?d[1-9][0-9]*$', flags=re.I)

    def is_valid_dice(self, arg):
        """ Uses regex to determine whether the dice roll is valid """
        return self.is_valid_dice_re.match(arg)

    @commands.command(hidden=False, brief="Roll the dice.")
    async def roll(self, ctx, dice='1d20'):
        """ Roll an XdY, where
                X = number of dice to roll (optional, default: 1)
                Y = number of sides on each die
            Default roll: 1d20
            Example rolls: 4d8, d6, 2d12

            Coming soon: support for modifiers """

        self.bot.logger.info(f'{ctx.author} rolls {dice}')
        await ctx.trigger_typing()

        try:

            if not self.is_valid_dice(dice):
                raise WegbotException(f'**{dice}** is not a valid dice roll')

            parts = dice.lower().split('d')

            count = int(parts[0]) if parts[0] else 1
            sides = int(parts[1])

            results = [ random.randint(1, sides) for i in range(count) ]
            total = sum(results)

            self.bot.logger.info(f'{ctx.author} rolls {dice}: {", ".join(results)}')
            self.bot.logger.info(f'{ctx.author} rolls {total} on {dice}')

            description = f'{ctx.author.mention} rolled **{total}** on **{count}d{sides}**.'
            if count > 1:
                description += f'\nRolls: **{"**, **".join([str(r) for r in results])}**'

            embedded = discord.Embed(title=f'Roll: {count}d{sides}', description=description)

            await ctx.send(embed=embedded)

        except WegbotException as ex:
            self.bot.logger.warning(f'invalid roll "{dice}" from {ctx.author}')
            await ctx.send(f"{ex.message}, {ctx.author.mention}.")

        except Exception as ex:
            self.bot.logger.exception(f'unexpected error rolling {dice}: {ex}')
            await ctx.send("Something went wrong.")

    @commands.command(hidden=False)
    async def flip(self, ctx, count='1'):
        """ Flip a coin.
            Flip multiple coins, I don't give a fuck """

        self.bot.logger.info(f'{ctx.author} flips {count}')
        await ctx.trigger_typing()

        try:

            count_i = int(count)
            if count_i < 1:
                raise WegbotException(f"I have no idea how to flip {count_i} coins")
            if count_i >= 100:
                raise WegbotException("I can't even count that high")
            if count_i > 10:
                raise WegbotException(f"{count_i} is too many coins")

            results = [ bool(random.randint(0, 1)) for i in range(int(count)) ]

            result_msg = f"{ctx.author.mention} flipped {count_i} coin(s).\n\n"

            if count_i == 1:
                result_msg += "Result: "
                result_msg += "**heads**" if results[0] is True else "**tails**"
            else:
                num_heads = len([ res for res in results if res is True ])
                num_tails = len([ res for res in results if res is False ])
                result_msg += f"Heads: **{num_heads}**\nTails: **{num_tails}**"

            embedded = discord.Embed(title=f"Flip: {count_i} coin(s)", description=result_msg)
            await ctx.send(embed=embedded)

        except WegbotException as ex:
            self.bot.logger.warning(f"can't flip {count}: {ex}")
            await ctx.send(f"{ex.message}, {ctx.author.mention}.")
        except ValueError:
            self.bot.logger.warning(f"invalid count {count} from {ctx.author}")
            await ctx.send(f"`{count}` isn't a number, {ctx.author.mention}.")
        except Exception as ex:
            self.bot.logger.exception(f"unexpected error flipping {count}: {ex}")
            await ctx.send(f"Unexpected error while flipping {count}. Check the logs.")



def setup(bot):
    bot.add_cog(Chance(bot))
