import asyncio
import json
import logging
import os
import traceback
import typing
import aiofiles
import aiohttp
import discord
import dotenv
import pendulum
from discord.ext import commands
from tortoise import Tortoise

from src import context, misc, models

DATABASE_CONNECTION_TRIES = 5


async def get_prefix(bot: "RoboDuck", message: discord.Message):
    await bot.wait_until_ready()

    if not message.guild:
        return commands.when_mentioned_or(bot.default_prefix)(bot, message)
        
    prefix = bot.guild_prefixes.get(message.guild.id)
    if not prefix:
        prefixes = await models.Prefixes.get_or_none(guild_id=message.guild.id)
        if prefixes:
            prefix = prefixes.prefix
            bot.guild_prefixes[message.guild.id] = prefixes.prefix
        else:
            prefix = bot.default_prefix

    return commands.when_mentioned_or(prefix)(bot, message)


class RoboDuck(commands.Bot):
    """
    A custom `commands.Bot` class to suit our needs.
    """

    def __init__(self):
        dotenv.load_dotenv()

        self.uptime = pendulum.now()
        
        self.guild_prefixes = {}
        self.guild_colors = {}

        self._logger = misc.create_logger("roboduck")
        self._prefix = os.getenv("PREFIX")
        
        self._emojis = None
        self._colors = None
        self._session = None

        super().__init__(
            command_prefix=get_prefix,
            intents=discord.Intents.all(),
            activity=discord.Game("🦆"),
            description="Quack!"
        )

    
    async def initialize_db(self):
        """Connect to a postgres database."""
        for i in range(DATABASE_CONNECTION_TRIES):
            try:
                await Tortoise.init(
                    db_url=os.getenv("DB_URL"), modules={"models": ["src.models"]},
                )
                self.logger.info("Connection to database successfull.")
                
                await Tortoise.generate_schemas()
                self.logger.info("Schemas generated.")
                
                colors = await models.Colors.all()
                for color in colors:
                    self.guild_colors[color.guild_id] = misc.Color(color.neutral, color.error, color.success)
                self.logger.info("Guild colors loaded.")
                
                return
            except Exception as ex:
                self.logger.error(
                    f"Connection to database failed. Retrying ... [{i}/{DATABASE_CONNECTION_TRIES}]",
                    exc_info=traceback.format_tb(ex.__traceback__),
                )
                await asyncio.sleep(5)
        else:
            self.logger.error("Connection to database can't be established.")

    async def start(self):
        """Overwrites the default start method to login with a token taken from the config."""
        await self.initialize_db()
        await self.load_emojis()
        await self.load_colors()
        self.load_extensions()

        async with aiohttp.ClientSession() as session:
            self._session = session
            await super().start(token=os.getenv("TOKEN"))

    async def close(self):
        """Close the connection to postgres aswell as discord."""
        await Tortoise.close_connections()
        return await super().close()

    def load_extensions(self):
        """Load all extensions in the specified `extensions_folder` path."""
        extensions_path = "src/extensions"
        for file in os.listdir(extensions_path):
            if file.endswith(".py") and not file.startswith("__init__"):
                try:
                    self.load_extension(
                        f"{extensions_path.replace('/', '.')}.{file.replace('.py', '')}"
                    )
                except Exception as ex:
                    self.logger.error(
                        "", exc_info=traceback.format_tb(ex.__traceback__)
                    )

        self.load_extension("jishaku")
        
    async def load_colors(self):
        """Loads colors from a `colors.json` file."""
        async with aiofiles.open("colors.json", "r") as file:
            file = json.loads(await file.read())
            self._colors = misc.Color(**file)

    async def load_emojis(self):
        """Loads emojis from a `emojis.json` file."""
        async with aiofiles.open("emojis.json", "r") as file:
            file = json.loads(await file.read())
            self._emojis = misc.DotDict(file)

    async def get_context(self, message, *, cls=None):
        """Custom context."""
        return await super().get_context(message, cls=cls or context.Context)    
    
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return

        return await self.process_commands(after)

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    @property
    def logger(self) -> logging.Logger:
        return self._logger
    
    @property
    def colors(self) -> misc.Color:
        return self._colors

    @property
    def default_prefix(self) -> str:
        return self._prefix