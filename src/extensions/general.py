import asyncio
import sys
import time

import discord
import pendulum
import psutil
from discord.ext import commands
from src import client


class General(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Pong!"""
        start_time = time.perf_counter()
        message = await ctx.send(
            embed=discord.Embed(
                color=discord.Color.lighter_grey(),
                description=f"{self.bot._emojis.get('loading')} Pinging ...",
            )
        )
        ack = (time.perf_counter() - start_time) * 1000
        heartbeat = self.bot.latency * 1000

        async with ctx.typing():
            embed = discord.Embed(color=ctx.get_color())
            embed.add_field(name="💓 Heartbeat:", value=f"`{heartbeat:,.2f}ms`")
            embed.add_field(name="🗄 ACK:", value=f"`{ack:,.2f}ms`")
            await message.delete()
            await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx: commands.Context):
        """General information about the bot"""
        embed = discord.Embed(
            color=ctx.get_color(),
            title=f"{self.bot._emojis.bot} About: {self.bot.user.name} | ID: {self.bot.user.id}",
            description=self.bot.description,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(
            name="Information",
            value=f"Owner ID: `{self.bot.owner_id}`\nUptime: {(pendulum.now() - self.bot.uptime).in_words(locale='en')}",
        )
        embed.add_field(
            name="Versions",
            value=f"{self.bot._emojis.get('python')} {sys.version.split(' ')[0]}\n{self.bot._emojis.get('discord')} {discord.__version__}",
            inline=False,
        )
        embed.add_field(
            name="Process",
            value=f"{self.bot._emojis.get('cpu')} {psutil.cpu_percent()}% / {round(psutil.cpu_freq().current, 2)}MHz\n{self.bot._emojis.get('ram')} {psutil.virtual_memory().percent}%",
        )
        # embed.add_field(name="Links", value=f"[Support Server]({self.bot.invite_url}) | [Invite]({self.bot.oauth()}) | [Source Code](https://github.com/illumfx/synth) | [Report a bug](https://github.com/illumfx/synth/issues) | [Website](https://illumfx.github.io/synth/)", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
