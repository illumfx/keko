import discord
from discord.ext import commands


class BaseView(discord.ui.View):
    def __init__(self, author: discord.Member, timeout=30):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.author:
            return True
        else:
            await interaction.response.send_message(
                content="You're not allowed to interact.", ephemeral=True
            )
            return False


class ConfirmView(BaseView):
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()


class DeleteView(discord.ui.View):
    def __init__(self, author: discord.Member, timeout):
        super().__init__(timeout=timeout)
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.author:
            return True
        else:
            await interaction.response.send_message(
                content="You're not allowed to interact.", ephemeral=True
            )
            return False

    @discord.ui.button(emoji="<:trash:859443116531777547>", style=discord.ButtonStyle.grey)
    async def _stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

