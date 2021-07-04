import discord  

class BaseView(discord.ui.View):
    def __init__(self, author: discord.Member, timeout = 30):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None
        
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.author:
            return True
        else:
            await interaction.response.send_message(content="You're not allowed to interact.", ephemeral=True)
            return False

class ConfirmView(BaseView): 
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        #await interaction.response.send_message("Confirmed", ephemeral=True)
        self.value = True
        self.stop()
        
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        #await interaction.response.send_message("Canceled", ephemeral=True)
        self.value = False
        self.stop()
        
class StopView(BaseView):
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def _stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        #await interaction.response.send_message("Stopped", ephemeral=True)
        self.value = False
        self.stop()