import asyncio
import json
import logging
import os
import platform
import traceback

import asyncpg
import discord
import dotenv
import pendulum
from discord.ext import commands

from bot import errors, misc

DATABASE_CONNECTION_TRIES = 5


class Bot(commands.Bot):
    """
    A custom `commands.Bot` class to suit our needs.
    """

    def __init__(self) -> None:
        """Opens the config."""
        dotenv.load_dotenv()

        self.env = misc.DotDict(os.environ)
        self.dev_mode = True if self.env.DEV.lower() == "true" else False
        self.logger = logging.getLogger(__name__)

        self.pool = None
        self.started = None

        self.errors = errors.Errors(self)

        super().__init__(
            command_prefix=os.environ.get("PREFIX") or "!",
            intents=discord.Intents.all(),
        )

    async def init_db(self) -> None:
        """Connect to the postgres database using environ"""
        if not self.dev_mode:
            for i in range(DATABASE_CONNECTION_TRIES):
                try:
                    pool = await asyncpg.connect(self.env.DB_URL)
                except:
                    self.logger.error(
                        f"Connection to database failed. Retrying ... [{i}/{DATABASE_CONNECTION_TRIES}]"
                    )
                    await asyncio.sleep(1.5)
                else:
                    self.logger.info("Connection to database successfull.")
                    self.pool = pool
            else:
                self.logger.error("Connection to database can't be established.")
        else:
            self.logger.warning(
                "Bot will not connect to database due to dev mode being on."
            )

    async def login(self, bot=True) -> None:
        """Overwrites the default login method to login with a token taken from the config.

        Args:
            bot (bool, optional): Should be True, because Userbots are not allowed.
        """
        await self.init_db()
        await super().login(token=self.env.TOKEN, bot=bot)
        # await self.change_startup_status()

        self.load_extensions()
        
    async def send_error(self, ctx, message):
        """Send a fancy error message
        """
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f"<a:cross:645198030256996352> {message}",
            timestamp=pendulum.now(),
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        return await ctx.reply(embed=embed)

    async def set_startup_status(self) -> None:
        await self.change_presence(
            activity=discord.Game("⛔ DEV MODE" if self.dev_mode else "🦆")
        )

    def load_extensions(self) -> None:
        """Load all extensions in the specified `extensions_folder` path."""
        extensions_path = "bot/extensions"
        for file in os.listdir(extensions_path):
            if file.endswith(".py") and not file.startswith("__init__"):
                try:
                    self.load_extension(
                        f"{extensions_path.replace('/', '.')}.{file.rstrip('.py')}"
                    )
                except Exception as ex:
                    traceback.print_exc()

        self.load_extension("libneko.extras.superuser")
        
