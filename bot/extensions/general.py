import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = [783729519160459264] # Setting in database in the future
        self.date_time_str = "yyyy-MM-dd'T'HH:mm:ss.SSSZ"

    @commands.command()
    async def sar(self, ctx: commands.Context, role: discord.Role):
        """Assignable roles system
        """
        if role.id in self.roles:
            embed = discord.Embed(color=discord.Color.green())
            if role not in ctx.author.roles:
                await ctx.author.add_roles(role)
                embed.description = f"Role {role.mention} given to {ctx.author.mention}."
            else:
                await ctx.author.remove_roles(role)
                embed.description = f"Role {role.mention} removed from {ctx.author.mention}."

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
