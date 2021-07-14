import asyncio
import typing
import discord
import pendulum

from discord.ext import commands
from src import views, models


class Context(commands.Context):  
    async def response(self, content: str = None, embed: discord.Embed = None):  
        if embed:   
            embed.timestamp = discord.utils.utcnow()
            embed.set_footer(
                text=f"Requested by {self.author}", icon_url=self.author.avatar.url
            )
            
        return await self.reply(content=content, embed=embed)

    async def confirm(
        self, message: str = "Do you want to confirm your action?", timeout=30
    ):
        """Confirm an action."""
        view = views.ConfirmView(author=self.author, timeout=timeout)
        message = await self.send(message, view=view)
        await view.wait()
        view.stop()
        if view.value is None:
            view.clear_items()
            await message.edit(content="Timed out ...", delete_after=10, view=view)
        else:
            await message.delete()
            return bool(view.value)
        
    async def waste(self, message: str = None, embed: discord.Embed = None, timeout=None):
        """Wastable message"""
        view = views.DeleteView(self.author, timeout)
        message = await self.send(message, embed=embed, view=view)
        await view.wait()
        await message.delete()
        try:
            await self.message.delete()
        except:
            pass

    async def select(self, options: list = ["test", "he"], timeout=30):
        """Select options."""

        def parse_options(options):
            for option in options:
                yield discord.SelectOption(label=option)

        view = views.SelectView(author=self.author, timeout=timeout)
        view.options = [so for so in parse_options(options)]

        message = await self.send("Select?", view=view)
        
    def get_color(self, color: str = None):
        color = color or "neutral"
        if guild_color := self.bot.guild_colors.get(self.guild.id, None):
            return discord.Color(int(guild_color.get(color) or self.bot.colors.get(color) or self.bot.colors.neutral))
        else:
            return discord.Color(int(self.bot.colors.get(color)))
