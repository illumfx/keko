import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Command
    async def db(self, ctx: commands.Context):
        """Test
        """
        await ctx.send("s")


def setup(bot):
    bot.add_cog(Test(bot))
