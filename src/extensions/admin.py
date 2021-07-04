import os

import aiohttp
import discord
from discord.ext import commands
from src import client, errors, misc


class Admin(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        if ctx.author.id == self.bot.owner_id:
            return True

        raise commands.NotOwner


def setup(bot):
    bot.add_cog(Admin(bot))
