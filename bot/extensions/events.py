import asyncio
import re
import traceback

import discord
import pendulum
from discord.ext import commands

from .. import errors, misc


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def bot_check(self, ctx):
        if self.bot.dev_mode:
            if not await self.bot.is_owner(ctx.author):
                raise errors.MessageException(
                    "`Dev Mode` is activated. Only commands from the bot owner will be executed."
                )

        return True

    @commands.Cog.listener()
    async def on_ready(self):
        """Checks if `bot.started` is defined. If it isn't, then it will get assigned with the current time. Status will get changed then."""
        if not self.bot.started:
            self.bot.started = pendulum.now()
            await self.bot.set_startup_status()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.name == "clips":
            if not re.match(r"(?:https:\/\/)?clips\.twitch\.tv\/", message.content):
                # await message.delete()
                pass

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        """The event triggered when an error is raised while invoking a command."""
        if hasattr(ctx.command, "on_error"):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error):
                return

        ignored = (commands.CommandNotFound,)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await self.bot.send_error(f"{ctx.command} has been disabled.")
        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            await self.bot.send_error(
                f"A parse or conversion error occured with your arguments. Check your input and try again. If you need help, use `{ctx.prefix}help {ctx.command.qualified_name or ctx.command.name}`"
            )
        elif isinstance(error, discord.Forbidden):
            await self.bot.send_error(
                "I'm unable to perform this action. This could happen due to missing permissions for the bot."
            )

        elif isinstance(error, commands.NotOwner):
            await self.bot.send_error(
                "This command is only available to the bot developer."
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            await self.bot.send_error(
                f"`{error.param.name}` is a required argument that is missing. For more help use `{ctx.prefix}help {ctx.command.qualified_name or ctx.command.name}`"
            )

        elif isinstance(error, commands.MissingPermissions):
            await self.bot.send_error("You're not allowed to use this command.")

        elif isinstance(error, commands.BotMissingPermissions):
            await self.bot.send_error(
                "I don't have enough permissions to execute this command."
            )

        elif isinstance(error, commands.NoPrivateMessage):
            await self.bot.send_error("This command is not usable in DM's.")

        elif isinstance(error, commands.CommandOnCooldown):
            await self.bot.send_error(
                f"You're on cooldown! Retry in `{error.retry_after:,.2f}` seconds."
            )

        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("❓")
            await asyncio.sleep(15)
            await ctx.message.remove_reaction(emoji="❓", member=ctx.guild.me)

        elif isinstance(error, errors.MessageException):
            await self.bot.send_error(error)

        elif isinstance(error, errors.CommandGroupInvoked):
            await ctx.send_help(ctx.command)

        else:
            saved_error = self.bot.errors.add_error(
                ctx, "".join(traceback.format_tb(error.__traceback__))
            )
            await self.bot.send_error(
                ctx,
                message=f"Unknown error occured. The bot developer has been notifed and the error will be fixed as soon as possible.\nReferral ID: `{saved_error.ref_id}`",
            )


def setup(bot):
    bot.add_cog(Events(bot))
