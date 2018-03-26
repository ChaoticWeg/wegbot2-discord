import discord
from discord.ext import commands

from cogs.errors import WegbotException

@commands.command(hidden=False, name="pin", brief="Pin a message.", rest_is_raw=True)
@commands.guild_only()
async def pin_that(self, ctx, message_id: int, *, addition=None):
    """ Pins the message with the given ID.

    You may also provide additional text that will appear at the front of the pinned message. """

    self.bot.logger.info(f'{ctx.author} request pin {message_id} in #{ctx.channel}')
    await ctx.trigger_typing()

    try:

        message = await ctx.channel.get_message(message_id)
        if message.pinned is True:
            raise WegbotException("That message is already pinned")

        embedded = discord.Embed(title=f"Message from {message.author}", description=addition)
        embedded.add_field(name="Original Message", value=message.content, inline=False)

        sent = await ctx.send(embed=embedded)
        await sent.pin()

    except WegbotException as ex:
        self.bot.logger.warning(f'wegbot exception while pinning {message_id}: {ex.message}')
        await ctx.send(f"{ex.message}, {ctx.author.mention}.")

    except discord.errors.NotFound:
        self.bot.logger.warning(f'attempted to pin message {message_id}, not found')
        await ctx.send(f"Couldn't find a message with that ID, {ctx.author.mention}.")

    except Exception as ex:
        self.bot.logger.warning(f'unable to pin message {message_id}: {ex}')
        await ctx.send(f"Couldn't pin that, {ctx.author.mention}. Have @ChaoticWeg check the logs.")
