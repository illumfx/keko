from asyncio.tasks import wait
import discord
from discord.ext import commands

from .. import models
from .. import extra

import datetime
import asyncio
import parsedatetime


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cal = parsedatetime.Calendar()
        self.mutes = extra.Mutes(bot)

    @commands.command()
    async def kick(self, ctx: commands.Context, member: discord.Member, reason=None):
        reason = reason or "No reason given"
        await member.kick(reason)

    @commands.command()
    async def ban(self, ctx: commands.Context, member: discord.Member, reason=None):
        reason = reason or "No reason given"
        await member.ban(reason)

    @commands.command()
    async def mute(self, ctx: commands.Context, target: discord.Member, *, until):
        datetime_obj, _ = self.cal.parseDT(datetimeString=until, tzinfo=datetime.timezone.utc)
        self.mutes.mute_member(target, datetime_obj)

        reason = None
        message = await ctx.send(embed=discord.Embed(color=discord.Color.green(), description=f"{target.mention} has been muted.\nPlease provide a reason."))
        def check(message: discord.Message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            reason = await self.bot.wait_for("message", check=check, timeout=15)
            await reason.add_reaction("👌")
        except asyncio.TimeoutError:
            reason = "No reason given"
            
        await message.edit(embed=discord.Embed(color=discord.Color.blue(), description=f"{target.mention} has been muted.\nReason: `{reason.content}`."))
        await models.Mutes.create(guild=ctx.guild.id, moderator=ctx.author.id, receiver=target.id, reason=reason.content, ends_at=datetime_obj)

    @commands.command()
    async def unmute(self, ctx: commands.Context, target: discord.Member):
        self.mutes.unmute_member(target)


def setup(bot):
    bot.add_cog(Moderation(bot))
