import os
import discord
import pendulum
import typing
import twitchio

from discord.ext import commands

from src import client, errors, misc


class Twitch(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot
        
        if not hasattr(bot, "twitch"):
            self.bot.twitch = twitchio.Client(
                client_id=os.getenv("TWITCH_CLIENT_ID"),
                client_secret=os.getenv("TWITCH_CLIENT_SECRET"),
            )
        self.twitch_icon = "https://i.gyazo.com/522eaf91e415a35f9e9c1aee71fd1ec1.png"

    @commands.group(invoke_without_command=True)
    async def twitch(self, ctx: commands.Context):
        """Couple commands dedicated to twitch.tv"""
        raise errors.CommandGroupInvoked

    @twitch.command()
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def stream(self, ctx: commands.Context, channel: typing.Union[str, int]):
        """Stream info for a channel"""
        if stream := await self.bot.twitch.get_stream(channel):
            stream = misc.DotDict(stream)
            embed = discord.Embed(
                color=discord.Color.purple(), description=stream.title
            )
            embed.set_author(
                name=f"{stream.user_name} is currently live!",
                url=f"https://www.twitch.tv/{stream.user_name}",
            )
            embed.set_footer(
                text=f"Stream start: {pendulum.parser.parse(stream.started_at).diff_for_humans()} | Viewer: {stream.viewer_count}",
                icon_url=self.twitch_icon,
            )
            embed.set_image(
                url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{stream.user_name.lower()}.jpg"
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.pretty_send(f"`{channel}` isn't live.", emoji="cross", color=discord.Color.red())

    @twitch.command()
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def top(self, ctx: commands.Context, limit: int = 10):
        """Top channels sorted by viewers"""
        if not limit < 10 or limit >= 1:
            await ctx.typing()
            top = await self.bot.twitch.get_top_games(limit)
            out = str()
            for game in top:
                out += f"[{game['name']}]({game['box_art_url'].format(width=285, height=380)}) | `{game['id']}`\n"
            embed = discord.Embed(color=discord.Color.purple(), description=out)
            embed.set_footer(text="Format: Name | ID", icon_url=self.twitch_icon)
            await ctx.reply(embed=embed)
        else:
            await ctx.pretty_send(f"`limit` can't be higher than 10 or lower than 1.", emoji="cross", color=discord.Color.red())


def setup(discord_bot):
    discord_bot.add_cog(Twitch(discord_bot))
