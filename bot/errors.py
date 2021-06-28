import secrets
from dataclasses import dataclass
from datetime import datetime
from logging import error
from typing import Tuple

import aiohttp
import discord
from discord.ext import commands


class MessageException(commands.CommandError):
    pass

class CommandGroupInvoked(commands.CommandError):
    pass


@dataclass
class Error:
    """Dataclass for keepinng track of errors.
    """
    ref_id: str
    traceback: str
    guild_id: int
    author_id: int
    command_name: str
    date: datetime = datetime.utcnow()
    
    def format(self):
        # """Guild ID: `{error.guild_id}`\nAuthor ID: `{error.author_id}`\nCommand Name: `{error.command_name}`\nArgs: `{', '.join(error.args)}`\nTraceback:\n```py\n{error.traceback.format()}```"""
        return f"""Guild ID: `{self.guild_id}`
    Author ID: `{self.guild_id}`
    Command: `{self.command_name}`
    Traceback: 
    ```py
    {self.traceback.format()}```
"""
    
class Errors:
    """Provides the ability to safe exceptions and look at them later by the `ref_id` attribute.
    """
    def __init__(self, bot) -> None:
        self.bot = bot
        self.webhook_url = bot.env.WEBHOOK_URL
        self.errors = {}
    
    def add_error(self, ctx: commands.Context, traceback) -> Error:
        ref_id = secrets.token_urlsafe(5)
        error = Error(ref_id=ref_id, traceback=traceback, guild_id=ctx.guild.id, author_id=ctx.author.id, command_name=ctx.command.qualified_name or ctx.command.name)
        self.errors[ref_id] = error
        #self.bot.loop.create_task(self.__send_error(error))
        return error
    
    def get_error(self, ref_id: str) -> Tuple[Error, None]:
        return self.errors.get(ref_id)
            
    def remove_error(self, ref_id: str) -> Tuple[Error, None]:
        return self.errors.pop(ref_id)
    
    async def __send_error(self, error: Error) -> None:
        async with aiohttp.ClientSession() as session:
            embed = discord.Embed(
                color=discord.Color.red(),
                title="🛑 An error occured",
                description=f"Referral ID: `{error.ref_id}`\nGuild ID: `{error.guild_id}`\nAuthor ID: `{error.author_id}`")
            
            webhook = discord.Webhook.from_url(self.webhook_url, adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(embed=embed)
