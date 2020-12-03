import discord
from discord.ext import commands

from ..extra import DotDict

from typing import Union
from datetime import datetime, timezone
import timeago
import dateutil.parser


class General(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.roles = [783729519160459264] # Setting in database in the future
        self.date_time_str = "yyyy-MM-dd'T'HH:mm:ss.SSSZ"

    @commands.Command
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

    @commands.Command
    async def stream(self, ctx: commands.Context, channel: Union[str, int]):
        """Stream info for a channel
        """
        if stream := await self.bot.twitch.get_stream(channel):
            stream = DotDict(stream)
            embed = discord.Embed(color=discord.Color.purple(), description=stream.title)
            embed.set_author(name=f"{stream.user_name} ist gerade live!", url=f"https://www.twitch.tv/{stream.user_name}")
            embed.set_footer(text=f"Stream start: {timeago.format(dateutil.parser.parse(stream.started_at), datetime.now(timezone.utc), locale='de')} | Zuschauer: {stream.viewer_count}")
            embed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{stream.user_name.lower()}.jpg")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"`{channel}` ist nicht Live.")


def setup(bot):
    bot.add_cog(General(bot))
