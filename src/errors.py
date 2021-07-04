from discord.ext import commands


class MessageException(commands.CommandError):
    pass

class CommandGroupInvoked(commands.CommandError):
    pass
