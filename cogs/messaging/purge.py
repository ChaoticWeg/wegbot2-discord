import os

import discord
from discord.ext import commands

from cogs.utils import _datetime as dt
from cogs.errors import WegbotException

@commands.command(hidden=True)
@commands.is_owner()
@commands.guild_only()
async def purge(self, ctx):
    """ Purge the channel.

    ** Unfortunately, due to Discord API limitations, only messages from within the last 14 days can be purged. Because fuck you."""

    await ctx.trigger_typing()

    try:

        if not str(ctx.channel.id) == os.getenv('DISCORD_HOME_CHANNEL'):
            raise WegbotException("I can't purge this channel")

        messages = await ctx.channel.history(limit=None, after=dt.earliest_message()).flatten()

        orig_num_messages = len(messages)

        print(f'purging {orig_num_messages} messages from #{str(ctx.channel)}... ', end='')

        while messages:
            # delete the first 100 messages if we need to, otherwise just delete them all
            temp_messages = messages[:100] if len(messages) > 100 else messages
            await ctx.channel.delete_messages(temp_messages)

            # chop off the first 100 messages if we need to. otherwise, we're done
            messages = messages[100:] if len(messages) > 100 else []

        await ctx.send(f"Purged {orig_num_messages} messages from {ctx.channel.mention} at the behest of {ctx.author.mention}.")

    except discord.ClientException:
        print('TOO MANY')
        blame = ctx.bot.get_user(int(os.getenv('DISCORD_OWNER'))).mention
        await ctx.send(f"Tried to purge too many messages at once! {blame} fucked up.")

    except discord.Forbidden:
        print('FORBIDDEN')
        await ctx.send(f"I don't have permission to purge this channel, {ctx.author.mention}.")

    except discord.HTTPException as ex:
        print('FAILED')
        await ctx.send("Something went wrong. Check the logs.")
        print(f'*** caught an HTTPException while trying to purge #{str(ctx.channel)}')
        print(ex)

    except Exception as ex:
        print('OWNED ONLINE')
        await ctx.send("Purge failed spectacularly. Check the logs.")
        raise ex

    else:
        print('OK')
