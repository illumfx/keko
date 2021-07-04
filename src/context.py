import discord
from discord import message
import pendulum
import typing
import asyncio

from discord.ext import commands
from src import views

class Context(commands.Context):   
    async def pretty_send(self, description: str, emoji: typing.Union[str, discord.Emoji, discord.PartialEmoji] = None, content: str = None, color: discord.Color = discord.Color.blurple()):
        """Sends a fancy standardized embed.
        """
        if isinstance(emoji, str):
            emoji = self.bot._emojis.get(emoji)
            
        embed = discord.Embed(
            color=color,
            description=f"{emoji} {description}" if emoji else description,
            timestamp=pendulum.now(),
        )
        embed.set_footer(text=f"Requested by {self.author}", icon_url=self.author.avatar.url)
        return await self.reply(content=content, embed=embed)
    
    async def confirm(self, message: str = "Do you want to confirm your action?", timeout=30):
        """Confirm an action.
        """
        view = views.ConfirmView(author=self.author, timeout=timeout)
        message = await self.send(message, view=view)
        await view.wait()
        await message.delete()
        view.stop()
        if view.value is None:
            await message.edit(content="Timed out ...")
        else:
            return bool(view.value)
        
    async def select(self, options: list = ["test", "he"], timeout=30):
        """Select options.
        """
        def parse_options(options):
            for option in options:
                yield discord.SelectOption(label=option)
                
        view = views.SelectView(author=self.author, timeout=timeout)
        view.options = [so for so in parse_options(options)]

        message = await self.send("Select?", view=view)
        
    
    @property
    def guild_manager(self):
        return self.bot.guild_manager.get_guild(self.guild.id)