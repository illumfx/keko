import os
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
