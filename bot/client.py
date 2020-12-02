import discord
from discord.ext import commands

from bot.extra import DotDict

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
        with open(os.environ.get("CONFIG_PATH")) as config_file:
            self.config_file = DotDict(json.load(config_file))

        self.logger = logging.getLogger(__name__)

        super().__init__(command_prefix=self.config_file.prefix)

    async def login(self, bot=True):
        """Overwrites the default login method to login with a token taken from the config.

        Args:
            bot (bool, optional): Should be True, because Userbots are not allowed.
        """
        self.load_extensions()
        await super().login(token=self.config_file.token, bot=bot)

    def load_extensions(self) -> None:
        """Load all extensions in the specified `extensions_folder` path.
        """
        for file in os.listdir(self.config_file.extensions_path):
            if file.endswith(".py") and not file.startswith("__init__"):
                try:
                    self.load_extension(
                        f"{self.config_file.extensions_path.replace('/', '.')}.{file.rstrip('.py')}")
                except Exception as ex:
                    traceback.print_exc()
