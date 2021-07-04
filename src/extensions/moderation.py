import asyncio
import datetime
import discord

from discord.ext import commands
from src import client, misc, models, errors


class Moderation(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot
        #self.cal = parsedatetime.Calendar()
        #self.mutes = extra.Mutes(bot)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, reason="No reason given"):
        """Ban a member."""
        await member.kick(reason)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, reason="No reason given"):
        """Kick a member."""
        await member.ban(reason)
        
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx: commands.Context):
        """Check current prefix."""
        prefixes = await models.Prefixes.get_or_none(guild_id=ctx.guild.id)
        if prefixes:
            await ctx.pretty_send(f"Current prefix for `{ctx.guild.name}` is: `{prefixes.prefix}`", emoji="info")
        else:       
            await ctx.pretty_send(f"Current prefix for `{ctx.guild.name}` is the default prefix (`{self.bot.default_prefix}`)", emoji="info")
        
    @prefix.command(name="remove")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix_remove(self, ctx: commands.Context):
        """Remove a prefix."""
        prefixes = await models.Prefixes.get_or_none(guild_id=ctx.guild.id)
        if prefixes:
            if await ctx.confirm(message=f"Do you want to remove the prefix for `{ctx.guild.name}`"):
                await prefixes.delete()
                await ctx.pretty_send(f"Prefix for `{ctx.guild.name}` is now the default prefix (`{self.bot.default_prefix}`).", emoji="check", color=discord.Color.green())
        else:
            await ctx.pretty_send(f"No custom prefix has been set, so it can't be removed.", emoji="cross", color=discord.Color.red()) 
        
    @prefix.command(name="set")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix_set(self, ctx: commands.Context, prefix: str):
        """Set a prefix, all other prefixes will be removed."""
        if prefix == self.bot.default_prefix:
            raise errors.MessageException(f"Prefix can't be the same as the default prefix (`{self.bot.default_prefix}`)")
        
        if await ctx.confirm(message=f"Do you want to change the prefix for `{ctx.guild.name}` to: `{prefix}`"):
            prefixes = await models.Prefixes.get_or_none(guild_id=ctx.guild.id)
            if prefixes:  
                    prefixes.prefix = prefix
                    await prefixes.save()
            else:
                await models.Prefixes.create(guild_id=ctx.guild.id, prefix=prefix)
                
            await ctx.pretty_send(f"Set `{prefix}` as prefix for `{ctx.guild.name}`.", emoji="check", color=discord.Color.green())

    # @commands.command()
    # async def mute(self, ctx: commands.Context, target: discord.Member, *, until):
    #     datetime_obj, _ = self.cal.parseDT(datetimeString=until, tzinfo=datetime.timezone.utc)
    #     self.mutes.mute_member(target, datetime_obj)

    #     reason = None
    #     message = await ctx.send(embed=discord.Embed(color=discord.Color.green(), description=f"{target.mention} has been muted.\nPlease provide a reason."))
    #     def check(message: discord.Message):
    #         return message.author == ctx.author and message.channel == ctx.channel
    #     try:
    #         reason = await self.bot.wait_for("message", check=check, timeout=15)
    #         await reason.add_reaction("👌")
    #     except asyncio.TimeoutError:
    #         reason = "No reason given"
            
    #     await message.edit(embed=discord.Embed(color=discord.Color.blue(), description=f"{target.mention} has been muted.\nReason: `{reason.content}`."))
    #     await models.Mutes.create(guild=ctx.guild.id, moderator=ctx.author.id, receiver=target.id, reason=reason.content, ends_at=datetime_obj)

    # @commands.command()
    # async def unmute(self, ctx: commands.Context, target: discord.Member):
    #     self.mutes.unmute_member(target)


def setup(bot):
    bot.add_cog(Moderation(bot))
