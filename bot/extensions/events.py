import discord
from discord.ext import commands

import re


class Events(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Filters a message out if the channel name is `clips`, must be a twitch clip
        """
        if message.channel.name == "clips":
            if not re.match(r"(?:https:\/\/)?clips\.twitch\.tv\/", message.content):
                await message.delete()


def setup(bot):
    bot.add_cog(Events(bot))
