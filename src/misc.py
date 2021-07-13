import logging
import typing

from dataclasses import dataclass

class DotDict(dict):
    """Access dictionary with dot notation."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
@dataclass
class Color:
    """Guild specific colors."""
    neutral: int
    error: int
    success: int
    
    def get(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            return None


class Cache:
    """Overall caching."""

    def __init__(self):
        self.cache = {}

    def add(self, attribute, value):
        if not self.is_valid(attribute):
            self.cache[attribute] = value

    def remove(self, attribute):
        return self.cache.pop(attribute)

    def get(self, attribute):
        return self.cache.__getitem__(attribute)

    def is_valid(self, attribute) -> bool:
        return attribute in self.cache

    def __str__(self):
        return str(self.cache)


def create_logger(name: str, level=logging.INFO):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger(name)
    logger.setLevel(level=level)

    sh = logging.StreamHandler()
    sh.setLevel(level=level)
    sh.setFormatter(formatter)

    logger.addHandler(sh)

    return logger


# TODO: Rewrite mute system


# class Mutes:
#     def __init__(self, bot) -> None:
#         self.bot = bot
#         self.tasks = dict()
#         bot.loop.create_task(self.__ainit__())

#     def mute_member(self, member: discord.Member, dt: datetime.datetime):
#         self.tasks[str(member.id)] = self.bot.loop.create_task(
#             self.__mute_member(member, dt))

#     def unmute_member(self, member: discord.Member):
#         self.bot.loop.create_task(self.__unmute_member(member))

#     async def __mute_member(self, member: discord.Member, dt: datetime.datetime):
#         role = await self.__get_role(member.guild)
#         if not role in member.roles:
#             await member.add_roles(role)

#         await self.__run_at(dt, self.__unmute_member(member))
#         await models.Mutes.delete(await models.Mutes.get(receiver=member.id, ends_at=dt))

#     async def __unmute_member(self, member: discord.Member):
#         role = await self.__get_role(member.guild)
#         if role in member.roles:
#             await member.remove_roles(role)

#         await models.Mutes.delete(await models.Mutes.get(receiver=member.id))
#         try:
#             self.tasks[str(member.id)].cancel()
#             del self.tasks[str(member.id)]
#         except:
#             pass

#     async def __get_role(self, guild: discord.Guild):
#         role = discord.utils.get(guild.roles, name="Muted")
#         if not role:
#             try:
#                 role = await guild.create_role(name="Muted")
#                 for category in guild.categories:
#                     try:
#                         await category.set_permissions(role, send_messages=False, connect=False, add_reactions=False)
#                     except:
#                         pass
#             except:
#                 pass

#         return role

#     async def __ainit__(self) -> None:
#         await self.bot.wait_until_ready()
#         async for mute in models.Mutes.all():
#             if guild := discord.utils.get(self.bot.guilds, id=mute.guild):
#                 if mute.ends_at > datetime.datetime.now(tz=datetime.timezone.utc):
#                     role = await self.__get_role(guild)

#                     self.mute_member(guild.get_member(mute.receiver), mute.ends_at)
#                 else:
#                     await self.__unmute_member(guild.get_member(mute.receiver))

#     async def __wait_until(self, dt):
#         now = datetime.datetime.now(tz=datetime.timezone.utc)
#         if dt > now:
#             await asyncio.sleep((dt - now).total_seconds())

#     async def __run_at(self, dt, coro):
#         await self.__wait_until(dt)

#         return await coro
