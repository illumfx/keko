import asyncio
import datetime

import discord
from discord import message
from discord.ext import commands
from src import client, errors, models, checks


class Moderation(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot
        # self.cal = parsedatetime.Calendar()
        # self.mutes = extra.Mutes(bot)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(
        self, ctx: commands.Context, member: discord.Member, reason="No reason given"
    ):
        """Ban a member."""
        await member.kick(reason)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self, ctx: commands.Context, member: discord.Member, reason="No reason given"
    ):
        """Kick a member."""
        await member.ban(reason)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx: commands.Context):
        """Check current prefix."""
        prefix = self.bot.guild_prefixes.get(ctx.guild.id, None)
        embed = discord.Embed(color=ctx.get_color(),
                              description=self.bot._emojis.info)
        if prefix:
            embed.description += f" Current prefix is: `{prefix}`"
        else:
            embed.description += f" Current prefix is the default prefix (`{self.bot.default_prefix}`)"
        await ctx.response(embed=embed)

    @prefix.command(name="reset")
    @commands.guild_only()
    @checks.is_owner_or_has_permissions(manage_guild=True)
    async def prefix_reset(self, ctx: commands.Context):
        """Reset a prefix."""
        if self.bot.guild_prefixes.get(ctx.guild.id, None):
            if await ctx.confirm(
                message=f"Do you want to reset the prefix?"
            ):
                await (await models.Prefixes.get(guild_id=ctx.guild.id)).delete()
                self.bot.guild_prefixes.pop(ctx.guild.id)

                embed = discord.Embed(color=ctx.get_color(
                    "success"), description=f"{self.bot._emojis.check} Prefix is now the default prefix (`{self.bot.default_prefix}`).")

                await ctx.response(embed=embed)
        else:
            embed = discord.Embed(color=ctx.get_color("error"), description=f"{self.bot._emojis.cross} No custom prefix has been set, so it can't be reset.")
            await ctx.response(embed=embed)

    @prefix.command(name="set")
    @commands.guild_only()
    @checks.is_owner_or_has_permissions(manage_guild=True)
    async def prefix_set(self, ctx: commands.Context, prefix: str):
        """Set a prefix, all other prefixes will be removed."""
        if prefix == self.bot.default_prefix:
            return await self.prefix_remove(ctx)

        if prefix == ctx.prefix:
            raise errors.MessageException(
                f"Prefix can't be the same as the current prefix."
            )

        if await ctx.confirm(
            message=f"Do you want to change the prefix to: `{prefix}`?"
        ):
            prefixes = await models.Prefixes.get_or_none(guild_id=ctx.guild.id)
            if prefixes:
                prefixes.prefix = prefix
                await prefixes.save()

            await models.Prefixes.create(guild_id=ctx.guild.id, prefix=prefix)

            embed = discord.Embed(color=ctx.get_color("success"), description=f"{self.bot._emojis.check} `{prefix}` has been set as prefix.")
            await ctx.response(embed=embed)

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
