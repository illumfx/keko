import asyncio
import sys
import time

import discord
import pendulum
import psutil
from discord.ext import commands
from src import client

class HelpCommand(commands.HelpCommand):
    def create_embed(self, color=None):
        ctx = self.context
        
        embed = discord.Embed(color=ctx.get_color(color))
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        return embed
    
    def get_cog_header(self, cog, commands):
        cog_name = getattr(cog, "qualified_name", "No Category")
        return f"{self.context.bot._emojis.whitedot} **{cog_name}** [` {len(commands)} `]"
    
    async def send_error_message(self, error):
        ctx = self.context
        
        embed = discord.Embed(color=self.context.get_color("error"))
        embed.description = f"{ctx.bot._emojis.cross} {error}"
        await ctx.response(embed=embed)
         
    # <prefix>help
    async def send_bot_help(self, mapping):
        ctx = self.context
        
        embed = self.create_embed()
        embed.description = f"{ctx.bot.description}\n*Use `{ctx.clean_prefix}help [category]` for more info on a category.*\n\n**Categories:**"
        embed.title = f"{ctx.bot._emojis.book} {ctx.bot.user.name} Help"
        embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        for cog, commands in mapping.items():
            if commands:
                embed.add_field(name=self.get_cog_header(cog, commands), value=getattr(cog, "description", "No description"), inline=False)
            
            # filtered = await self.filter_commands(commands, sort=True)
            # command_signatures = [self.get_command_signature(c) for c in filtered]
            # if command_signatures:
            #     cog_name = getattr(cog, "qualified_name", "No Category")
            #     embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
                
        await ctx.waste(embed=embed)
    
    # <prefix>help <command>
    async def send_command_help(self, command):
        ctx = self.context
        
        embed = self.create_embed()
        embed.title = command.qualified_name
        embed.add_field(name="Help", value=command.help, inline=False)
        embed.add_field(name="Signature", value=self.get_command_signature(command), inline=False)
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
            
        await ctx.waste(embed=embed)
    
    # <prefix>help <group>
    async def send_group_help(self, group):
        ctx = self.context
        
        filtered = await self.filter_commands(group.commands, sort=True)
        command_signatures = [self.get_command_signature(c) for c in filtered]
        
        embed = self.create_embed()
        embed.title = group.name
        embed.description =f"Help for `{group.name}` command group.\nUse `{ctx.clean_prefix}help {group.name} [command]` for more info on a subcommand."
        embed.add_field(name="Subcommands", value="\n".join(command_signatures), inline=False)
        
        await ctx.waste(embed=embed)
    
    # <prefix>help <cog>
    async def send_cog_help(self, cog):
        ctx = self.context
        
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        command_signatures = [self.get_command_signature(c) for c in filtered]
        
        embed = self.create_embed()
        embed.title = cog.qualified_name
        embed.description =f"Help for `{cog.qualified_name}` category.\nUse `{ctx.clean_prefix}help [command]` for more info on a command."
        embed.add_field(name="Commands", value="\n".join(command_signatures), inline=False)
        
        await ctx.waste(embed=embed)
    
    def get_command_signature(self, command):
        return "{0.context.clean_prefix}{1.qualified_name} {1.signature}".format(self, command)

class General(commands.Cog):
    """General commands"""
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot
        self.__help_command = bot.help_command
        help_command = HelpCommand()
        help_command.cog = self
        bot.help_command = help_command
        
    def cog_unload(self):
        self.bot.help_command = self.__help_command

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Pong!"""
        start_time = time.perf_counter()
        message = await ctx.send(
            embed=discord.Embed(
                color=discord.Color.lighter_grey(),
                description=f"{self.bot._emojis.get('loading')} Pinging ...",
            )
        )
        ack = (time.perf_counter() - start_time) * 1000
        heartbeat = self.bot.latency * 1000

        async with ctx.typing():
            embed = discord.Embed(color=ctx.get_color())
            embed.add_field(name="💓 Heartbeat:", value=f"`{heartbeat:,.2f}ms`")
            embed.add_field(name="🗄 ACK:", value=f"`{ack:,.2f}ms`")
            await message.delete()
            await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx: commands.Context):
        """General information about the bot"""
        embed = discord.Embed(
            color=ctx.get_color(),
            title=f"{self.bot._emojis.bot} About: {self.bot.user.name} | ID: {self.bot.user.id}",
            description=self.bot.description,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(
            name="Information",
            value=f"Owner ID: `{self.bot.owner_id}`\nUptime: {(pendulum.now() - self.bot.uptime).in_words(locale='en')}",
        )
        embed.add_field(
            name="Versions",
            value=f"{self.bot._emojis.get('python')} {sys.version.split(' ')[0]}\n{self.bot._emojis.get('discord')} {discord.__version__}",
            inline=False,
        )
        embed.add_field(
            name="Process",
            value=f"{self.bot._emojis.get('cpu')} {psutil.cpu_percent()}% / {round(psutil.cpu_freq().current, 2)}MHz\n{self.bot._emojis.get('ram')} {psutil.virtual_memory().percent}%",
        )
        # embed.add_field(name="Links", value=f"[Support Server]({self.bot.invite_url}) | [Invite]({self.bot.oauth()}) | [Source Code](https://github.com/illumfx/synth) | [Report a bug](https://github.com/illumfx/synth/issues) | [Website](https://illumfx.github.io/synth/)", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
