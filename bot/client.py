import discord
from discord.ext import commands

from bot.extra import DotDict
from bot.db import init_db
from bot.twitch import TwitchClient

import os
import json
import traceback
import dotenv
import logging


class CustomBot(commands.Bot):
    """
    A custom `commands.Bot` class to suit our needs.
    """

    def __init__(self) -> None:
        """Opens the config.
        """
        dotenv.load_dotenv()
        self.env = DotDict(os.environ)

        self.logger = logging.getLogger(__name__)

        self.twitch = TwitchClient(self.env)
        super().__init__(command_prefix=os.environ.get("PREFIX") or "?")

    async def login(self, bot=True):
        """Overwrites the default login method to login with a token taken from the config.

        Args:
            bot (bool, optional): Should be True, because Userbots are not allowed.
        """
        #await init_db(self.env)
        await super().login(token=self.env.TOKEN, bot=bot)
        self.load_extensions()

    def load_extensions(self) -> None:
        """Load all extensions in the specified `extensions_folder` path.
        """
        extensions_path = "bot/extensions"
        for file in os.listdir(extensions_path):
            if file.endswith(".py") and not file.startswith("__init__"):
                try:
                    self.load_extension(
                        f"{extensions_path.replace('/', '.')}.{file.rstrip('.py')}")
                except Exception as ex:
                    traceback.print_exc()
