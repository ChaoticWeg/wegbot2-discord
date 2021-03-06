import discord
from discord.ext import commands

from cogs.utils import _datetime as dt

THRESHOLD = 5

@commands.command(brief="Please don't @everyone.")
async def nuisance(self, ctx, *, whomst: commands.UserConverter):
    """
    Do you have a friend who won't quit @'ing everyone? Tag them. Shame them.
    ...Or vindicate them. You might just be a prick about it.

    But are they a nuisance? I'll be the judge of that."""

    await ctx.trigger_typing()

    history = []

    for channel in ctx.guild.text_channels:
        try:
            history.extend(await channel.history(limit=None, after=dt.earliest_message()).flatten())
        except:
            pass

    nuisances = len([ m for m in history if m.author == whomst and m.mention_everyone ])

    embed_title = f"{whomst.name} IS{'' if nuisances >= THRESHOLD else ' NOT'} a nuisance"
    embed_desc = f"I see {nuisances} mention(s) of `@everyone` or `@here` in the last 14 days."

    embedded = discord.Embed(title=embed_title, description=embed_desc)
    embedded.set_footer(text="(just don't do it)")

    await ctx.send(embed=embedded)
