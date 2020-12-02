import discord
from discord.ext import commands

import aiohttp


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def cog_check(self, ctx: commands.Context):
        if not ctx.author.id in self.bot.config_file.owner_ids:
            return await ctx.send("Nö.")

        return True

    @commands.group()
    async def manage(self, ctx: commands.Context):
        """Change bot settings, appearence, etc ...
        """
        pass

    @manage.command()
    async def name(self, ctx: commands.Context, *, name: str):
        """Change bot name
        """
        await self.bot.user.edit(username=name)
        await ctx.send(f"Name geändert zu: `{name}`.")

    @manage.command()
    async def avatar(self, ctx: commands.Context):
        """Change avatar, need to provide an attachment
        """
        if ctx.message.attachments:
            async with self.session.get(ctx.message.attachments[0].url) as resp:
                if resp.content_type.startswith("image"):
                    await self.bot.user.edit(avatar=await resp.read())
                    await ctx.send("Profilbild geändert.")
                else:
                    await ctx.send("Anhang ist kein Bild.")
        else:
            await ctx.send("Du musst einen Anhang anhängen.")


def setup(bot):
    bot.add_cog(Admin(bot))
