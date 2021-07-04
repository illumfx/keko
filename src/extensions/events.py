import discord
import aiohttp
import traceback
import os

from discord.ext import commands

from src import client, errors, misc, models

twitch_clip_rx = r"(?:https:\/\/)?clips\.twitch\.tv\/"

class Events(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return
        
        if message.guild and self.bot.user.mentioned_in(message) and len(message.content.strip(self.bot.user.mention)) == 1:
            prefixes = await models.Prefixes.get_or_none(guild_id=message.guild.id)
            ctx = await self.bot.get_context(message)
            if prefixes:     
                await ctx.pretty_send(f"My prefix for **{message.guild.name}** is: `{prefixes.prefix}`.", emoji="info", color=discord.Color.blurple())
            else:
                await ctx.pretty_send(f"My prefix for **{message.guild.name}** is the default prefix (`{self.bot.default_prefix}`).", emoji="info", color=discord.Color.blurple())
         
    @commands.Cog.listener()   
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        print(before)
        
        if before.author.bot:
            return
        
        if before == after:
            return
        
        await self.bot.process_commands(after)

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
            await ctx.pretty_send(description=f"{ctx.command} has been disabled.", emoji="cross", color=discord.Color.red())
            
        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            await ctx.pretty_send(description=f"A parse or conversion error occured with your arguments. Check your input and try again. If you need help, use `{ctx.prefix}help {ctx.command.qualified_name or ctx.command.name}`", emoji="cross", color=discord.Color.red())
            
        elif isinstance(error, discord.Forbidden):
            await ctx.pretty_send(description="I'm unable to perform this action. This could happen due to missing permissions for the bot.", emoji="cross", color=discord.Color.red())

        elif isinstance(error, commands.NotOwner):
            await ctx.pretty_send(description="This command is only available to the bot developer.", emoji="cross", color=discord.Color.red())

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.pretty_send(description=f"`{error.param.name}` is a required argument that is missing. For more help use `{ctx.prefix}help {ctx.command.qualified_name or ctx.command.name}`", emoji="cross", color=discord.Color.red())

        elif isinstance(error, commands.MissingPermissions):
            await ctx.pretty_send(description=f"You're missing {', '.join(error.missing_perms)} permission(s).", emoji="cross", color=discord.Color.red())

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.pretty_send(description=f"I'am missing {', '.join(error.missing_perms)} permission(s).", emoji="cross", color=discord.Color.red())

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.pretty_send(description="This command is not usable in DM's.", emoji="cross", color=discord.Color.red())

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.pretty_send(description=f"You're on cooldown! Retry in `{error.retry_after:,.2f}` seconds.", emoji="cross", color=discord.Color.red())
            
        elif isinstance(error, errors.MessageException):
            await ctx.pretty_send(description=error, emoji="cross", color=discord.Color.red())

        elif isinstance(error, errors.CommandGroupInvoked):
            await ctx.send_help(ctx.command)

        else:
            self.bot.logger.error("", exc_info=error)
            await ctx.pretty_send(description=f"Unknown error occured. The bot developer has been notifed and the error will be fixed as soon as possible.", emoji="cross", color=discord.Color.red())
            
            async with aiohttp.ClientSession() as session:
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title="🛑 An error occured",
                    description=f"Guild: {ctx.guild} (`{ctx.guild.id}`)\nAuthor: {ctx.author} (`{ctx.author.id}`)\n\n```py\n{error.__traceback__}```")
                
                webhook = discord.Webhook.from_url(os.getenv("WEBHOOK_URL"), session=self.bot.session)
                await webhook.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
