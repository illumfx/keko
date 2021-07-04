import discord

from discord.ext import commands
from src import client

class General(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot

def setup(bot):
    bot.add_cog(General(bot))
