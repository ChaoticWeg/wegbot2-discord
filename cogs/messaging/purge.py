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

    self.bot.logger.info(f'{ctx.author} request purge #{ctx.channel}')
    await ctx.trigger_typing()

    try:

        if not str(ctx.channel.id) == os.getenv('DISCORD_HOME_CHANNEL'):
            raise WegbotException("I can't purge this channel")

        messages = await ctx.channel.history(limit=None, after=dt.earliest_message()).flatten()

        orig_num_messages = len(messages)

        self.bot.logger.info(f'purging {orig_num_messages} messages from {str(ctx.channel)}')

        while messages:
            # delete the first 100 messages if we need to, otherwise just delete them all
            temp_messages = messages[:100] if len(messages) > 100 else messages
            await ctx.channel.delete_messages(temp_messages)

            # chop off the first 100 messages if we need to. otherwise, we're done
            messages = messages[100:] if len(messages) > 100 else []

        await ctx.send(f"Purged {orig_num_messages} messages from {ctx.channel.mention} at the behest of {ctx.author.mention}.")

    except discord.ClientException as ex:
        self.bot.logger.warning('tried to purge too many messages (or other ClientException)')
        self.bot.logger.warning(ex)

        blame = ctx.bot.get_user(int(os.getenv('DISCORD_OWNER'))).mention
        await ctx.send(f"Tried to purge too many messages at once! {blame} fucked up.")

    except discord.Forbidden:
        self.bot.logger.warning(f"{ctx.author} tried to purge a channel we don't have access to ({ctx.channel})")
        await ctx.send(f"I don't have permission to purge this channel, {ctx.author.mention}.")

    except discord.HTTPException as ex:
        self.bot.logger.warning(f'failed to purge {ctx.channel}: {ex}')
        await ctx.send("Something went wrong. Check the logs.")

    except Exception as ex:
        self.bot.logger.warning(f'unexpected error purging {ctx.channel}: {ex}')
        await ctx.send("Purge failed spectacularly. Check the logs.")
        raise ex

    else:
        self.bot.logger.info(f'successfully purged {ctx.channel}')
