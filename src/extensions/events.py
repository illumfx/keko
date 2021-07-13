from datetime import datetime
import os
import traceback

import aiohttp
import discord
from discord.ext import commands
from src import client, errors, misc, models

twitch_clip_rx = r"(?:https:\/\/)?clips\.twitch\.tv\/"


class Events(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if (
            message.guild
            and self.bot.user.mentioned_in(message)
            and len(message.content.strip(self.bot.user.mention)) == 1
        ):
            prefix = self.bot.guild_prefixes.get(message.guild.id, self.bot.default_prefix)
            ctx = await self.bot.get_context(message)
            embed = discord.Embed(color=ctx.get_color(), description=f"{self.bot._emojis.info} My prefix for **{message.guild.name}** is: `{prefix}`.")
            await ctx.reply(embed=embed)


    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        """The event triggered when an error is raised while invoking a command."""
        
        async def __send_error(description: str):
            embed = discord.Embed(color=ctx.get_color("error"), description=self.bot._emojis.cross + description)
            await ctx.response(embed=embed)
        
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
            await __send_error(f"{ctx.command} has been disabled.")

        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            await __send_error(f"A parse or conversion error occured with your arguments. Check your input and try again. If you need help, use `{ctx.prefix}help {ctx.command.qualified_name or ctx.command.name}`")

        elif isinstance(error, discord.Forbidden):
            await __send_error(f"I'm unable to perform this action. This could happen due to missing permissions for the bot.")

        elif isinstance(error, commands.NotOwner):
            await __send_error(f"This command is only available to the bot developer.")

        elif isinstance(error, commands.MissingRequiredArgument):
            await __send_error(f"`{error.param.name}` is a required argument that is missing. For more help use `{ctx.prefix}help {ctx.command.qualified_name or ctx.command.name}`")

        elif isinstance(error, commands.MissingPermissions):
            await __send_error(f"You're missing {', '.join(error.missing_permissions)} permission(s).")

        elif isinstance(error, commands.BotMissingPermissions):
            await __send_error(f"I'am missing {', '.join(error.missing_permissions)} permission(s).")

        elif isinstance(error, commands.NoPrivateMessage):
            await __send_error(f"This command is not usable in DM's.")

        elif isinstance(error, commands.CommandOnCooldown):
            await __send_error(f"You're on cooldown! Retry in `{error.retry_after:,.2f}` seconds.")

        elif isinstance(error, errors.MessageException):
            await __send_error(error)

        elif isinstance(error, errors.CommandGroupInvoked):
            await ctx.send_help(ctx.command)

        else:
            self.bot.logger.error("", exc_info=error)
            await __send_error(f"Unknown error occured. The bot developer has been notifed and the error will be fixed as soon as possible.")

            async with aiohttp.ClientSession() as session:
                description = (
                    f"Guild: {ctx.guild} (`{ctx.guild.id}`)" if ctx.guild else ""
                )
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title="🛑 An error occured",
                    description=description
                    + f"\nAuthor: {ctx.author} (`{ctx.author.id}`)\nCommand: `{ctx.command.qualified_name}`\nTimestamp: {discord.utils.format_dt(datetime.utcnow(), 'F')}",
                )

                webhook = discord.Webhook.from_url(
                    os.getenv("WEBHOOK_URL"), session=self.bot.session
                )
                await webhook.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
