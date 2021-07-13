import typing

import discord
from discord.ext import commands
from src import client, models, views


class SelectSelfAssignableRoles(discord.ui.Select):
    def __init__(self, author: discord.Member, placeholder: str = "Placeholder"):
        self.author = author
        self.roles = author.roles
        super().__init__(placeholder=placeholder)

    async def callback(self, interaction: discord.Interaction):
        role = discord.utils.get(self.author.guild.roles, id=int(self.values[0]))
        embed = interaction.message.embeds[0]
        embed.clear_fields()
        if role in self.author.roles:
            self.roles.remove(role)
            await self.author.remove_roles(role)
            embed.add_field(
                name="Current Action",
                value=f"Role {role.mention} removed from {self.author.mention}.",
                inline=False,
            )
        else:
            self.roles.append(role)
            await self.author.add_roles(role)
            embed.add_field(
                name="Current Action",
                value=f"Role {role.mention} given to {self.author.mention}.",
                inline=False,
            )

        embed.description = f'{", ".join([role.mention for role in sorted(self.roles) if not role.name == "@everyone"])}'

        await interaction.message.edit(embed=embed)


class SelfAssignableRoles(commands.Cog):
    def __init__(self, bot: client.RoboDuck):
        self.bot = bot
        
    def cog_check(self, ctx: commands.Context):
        if ctx.command.qualified_name != "sar":
            return bool(ctx.author.guild_permissions.manage_guild)
        return True

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(manage_roles=True)
    async def sar(self, ctx: commands.Context):
        """Opens the self assignable roles view."""
        view = views.StopView(ctx.author)
        select = SelectSelfAssignableRoles(ctx.author, placeholder="Select a role ...")
        try:
            roles = (await models.SelfAssignableRoles.get(guild_id=ctx.guild.id)).roles

            for role in roles:
                role = ctx.guild.get_role(role)
                select.add_option(
                    label=f"{role.name}",
                    value=str(role.id),
                    emoji=self.bot._emojis.get("whitedot"),
                    description=str(role.id),
                )

            view.add_item(select)

            embed = discord.Embed(color=discord.Color.blurple())
            embed.set_author(
                name=f"Roles for {ctx.author}:", icon_url=ctx.author.avatar.url
            )
            embed.add_field(
                name="Last Action", value="Nothing changed yet ...", inline=False
            )
            embed.description = f'{", ".join([role.mention for role in ctx.author.roles if not role.name == "@everyone"])}'

            message = await ctx.send(embed=embed, view=view)
            await view.wait()

            if view.value is False:
                await message.delete()
                view.stop()
        except:
            await ctx.pretty_send(
                "Self assignable roles haven't been set up yet.",
                emoji="cross",
                color=discord.Color.red(),
            )

    @sar.command(name="add")
    async def sar_add(self, ctx: commands.Context, role: discord.Role):
        """Add a role to self assignable roles."""
        if role > ctx.guild.me.top_role:
            return ctx.pretty_send(
                f"{role.mention} is higher in the hierarchy than me.",
                emoji="cross",
                color=discord.Color.red(),
            )

        sar = await models.SelfAssignableRoles.get_or_none(guild_id=ctx.guild.id)

        if sar:
            if role.id in sar.roles:
                await ctx.pretty_send(
                    f"{role.mention} already in self assignable roles.",
                    emoji="cross",
                    color=discord.Color.red(),
                )

            sar.roles.append(role.id)
            await sar.save()
        else:
            await models.SelfAssignableRoles.create(
                guild_id=ctx.guild.id, roles=[role.id]
            )

        await ctx.pretty_send(
            f"Added {role.mention} to self assignable roles.",
            emoji="check",
            color=discord.Color.green(),
        )

    @sar.command(name="remove")
    async def sar_remove(self, ctx: commands.Context, role: discord.Role):
        """Remove a role from self assignable roles."""
        if role > ctx.guild.me.top_role:
            return await ctx.pretty_send(
                f"{role.mention} is higher in the hierarchy than me.",
                emoji="cross",
                color=discord.Color.red(),
            )

        sar = await models.SelfAssignableRoles.get_or_none(guild_id=ctx.guild.id)

        if sar:
            if role.id not in sar.roles:
                await ctx.pretty_send(
                    f"{role.mention} not in self assignable roles.",
                    emoji="cross",
                    color=discord.Color.red(),
                )

            sar.roles.remove(role.id)
            await sar.save()
        else:
            await sar.delete()

        await ctx.pretty_send(
            f"Removed {role.mention} from self assignable roles.",
            emoji="check",
            color=discord.Color.green(),
        )


def setup(bot):
    bot.add_cog(SelfAssignableRoles(bot))
