import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.roles = bot.config_file.assignable_roles

    @commands.Command()
    async def sar(self, ctx: commands.Context, role: discord.Role):
        """Assignable roles system
        """
        if role.id in self.roles:
            embed = discord.Embed(color=discord.Color.green())
            if role not in ctx.author.roles:
                await ctx.author.add_roles(role)
                embed.description = f"Rolle {role.mention} an {ctx.author.mention} vergeben."
            else:
                await ctx.author.remove_roles(role)
                embed.description = f"Rolle {role.mention} von {ctx.author.mention} weggenommen."

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
