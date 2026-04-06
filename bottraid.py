import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os

# TOKEN pobierany z zakładki Variables w Railway
TOKEN = os.getenv('MTQ5MDc1MzQxNTc2MjkzOTk5Nw.GrrhQo.ekBIKV2PetAixyOSzWznocRKo29cc492uR9vzk')

class RaidControlView(discord.ui.View):
    def __init__(self, text):
        super().__init__(timeout=None)
        self.text = text
        self.invite_link = "https://discord.gg/Wtvpn5jZ"

    async def send_clean_packet(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.text,
            description=f"**Dołącz do nas:**\n{self.invite_link}",
            color=0x2b2d31
        )
        embed.set_footer(text="SecretRaid System • Operacja Aktywna")
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Wyślij 1x", style=discord.ButtonStyle.primary)
    async def send_1x(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await self.send_clean_packet(interaction)

    @discord.ui.button(label="Wyślij 5x", style=discord.ButtonStyle.secondary)
    async def send_5x(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        for i in range(5):
            await self.send_clean_packet(interaction)
            await asyncio.sleep(0.4)
        
        await interaction.followup.send(
            "✅ Seria wysłana. System gotowy:", 
            view=RaidControlView(self.text), 
            ephemeral=True
        )

class SecretRaid(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Zalogowano jako {self.user}")

bot = SecretRaid()

@bot.tree.command(name="spam", description="Odpala panel SecretRaid")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def spam(interaction: discord.Interaction, wiadomosc: str):
    view = RaidControlView(wiadomosc)
    await interaction.response.send_message("⚙️ **PANEL SECRETRAID**", view=view, ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)
