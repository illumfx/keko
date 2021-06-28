import aiohttp
import discord
from bot import errors, misc
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        if ctx.author.id == self.bot.env.OWNER_ID:
            return True

        raise commands.NotOwner

    @commands.group(invoke_without_command=True)
    async def errors(self, ctx: commands.Context):
        """Internal error handling stuff"""
        raise errors.CommandGroupInvoked

    @errors.command(name="show")
    async def errors_show(self, ctx: commands.Context, ref_id: str):
        if error := self.bot.errors.get_error(ref_id):
            embed = discord.Embed(
                color=discord.Color.blurple(),
                description=error.format(),
                timestamp=error.date,
            )
            embed.set_footer(text="Error occured")
            await ctx.reply(embed=embed)
        else:
            await self.bot.send_error(
                ctx=ctx, message=f"Error with referral id `{ref_id}` couldn't be found."
            )

    @errors.command(name="remove")
    async def errors_remove(self, ctx: commands.Context):
        await ctx.send("")

    @commands.command()
    async def test(self, ctx):
        await ctx.send(int("he4h"))


def setup(bot):
    bot.add_cog(Admin(bot))
