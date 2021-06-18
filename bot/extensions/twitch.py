import discord
from discord.ext import commands
from twitchio import Client

from ..extra import DotDict

from typing import Union
from datetime import datetime, timezone
import timeago
import dateutil.parser

class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.twitch = Client(
            client_id = bot.env.TWITCH_CLIENT_ID,
            client_secret = bot.env.TWITCH_CLIENT_SECRET
        )
        self.twitch_icon = "https://i.gyazo.com/522eaf91e415a35f9e9c1aee71fd1ec1.png"
        
    @commands.group()
    async def twitch(self, ctx: commands.Context):
        """Couple commands dedicated to twitch.tv
        """
        pass
        
    @twitch.command()
    async def stream(self, ctx: commands.Context, channel: Union[str, int]):
        """Stream info for a channel
        """
        if stream := await self.bot.twitch.get_stream(channel):
            stream = DotDict(stream)
            embed = discord.Embed(color=discord.Color.purple(), description=stream.title)
            embed.set_author(name=f"{stream.user_name} is currently live!", url=f"https://www.twitch.tv/{stream.user_name}")
            embed.set_footer(text=f"Stream start: {timeago.format(dateutil.parser.parse(stream.started_at), datetime.now(timezone.utc), locale='de')} | Viewer: {stream.viewer_count}", icon_url=self.twitch_icon)
            embed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{stream.user_name.lower()}.jpg")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"`{channel}` isn't live.")
            
    @twitch.command()
    async def top(self, ctx: commands.Context, limit: int = 10):
        """Top channels sorted by viewers
        """
        if not limit < 10 or limit >= 1:
            top = await self.bot.twitch.get_top_games(limit)
            out = str()
            for game in top:
                out += f"[{game['name']}]({game['box_art_url'].format(width=285, height=380)}) | `{game['id']}`\n"
            embed = discord.Embed(color=discord.Color.purple(), description=out)
            embed.set_footer(text="Format: Name | ID ()", icon_url=self.twitch_icon)
            await ctx.send(embed=embed)
        
def setup(discord_bot):
    discord_bot.add_cog(Twitch(discord_bot))