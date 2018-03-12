from datetime import datetime, timedelta
import os

import discord
from discord.ext import commands

from .errors import WegbotException

class Messaging:
    """ Message-related commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False, name="pin")
    @commands.guild_only()
    async def pin_that(self, ctx, *, target_user: commands.UserConverter):
        await ctx.trigger_typing()

        try:

            messages = await ctx.channel.history(limit=10).flatten()
            message_ids = [ msg.id for msg in messages if msg.author == target_user ]
            messages = [ msg for msg in messages if msg.id in message_ids ]

            if not message_ids:
                raise WegbotException(f"{target_user.name} hasn't said anything recently")

            message = messages[0]

            if message.author == ctx.author:
                raise WegbotException("You can't use me to pin your own comment")

            if message.author == self.bot.user:
                raise WegbotException("I won't pin my own message")

            await message.pin()

        except WegbotException as ex:
            await ctx.send(f"{ex.message}, {ctx.author.mention}.")

        except Exception as ex:
            print(ex)
            await ctx.send(f"Couldn't pin that, {ctx.author.mention}.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def purge(self, ctx):
        """ Purge the channel.

        ** Unfortunately, due to Discord API limitations, only messages from within the last 14 days can be purged. Because fuck you."""

        try:

            if not str(ctx.channel.id) == os.getenv('DISCORD_HOME_CHANNEL'):
                raise WegbotException("I can't purge this channel")

            async with ctx.typing():
                now = datetime.utcnow()
                earliest = now - timedelta(days=14)

                messages = await ctx.channel.history(limit=None, after=earliest).flatten()

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


def setup(bot):
    bot.add_cog(Messaging(bot))
