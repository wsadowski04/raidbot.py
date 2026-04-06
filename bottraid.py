import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os  # <-- DODAJ ten import do obsługi zmiennych środowiskowych

# UWAGA: NIGDY NIE UMIESZCZAJ TOKENA BEZPOŚREDNIO W KODZIE!
# Pobierz token ze zmiennej środowiskowej, którą za chwilę skonfigurujemy.
TOKEN = os.getenv('MTQ5MDc1MzQxNTc2MjkzOTk5Nw.Gal-fX.6bxEjOumXu235aEudNpqzOFUcPPcXO4iWZrmYY')

# Sprawdź, czy token został pobrany, jeśli nie – zakończ działanie.
if not TOKEN:
    print("Błąd krytyczny: Nie znaleziono zmiennej środowiskowej DISCORD_TOKEN.")
    exit(1)

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
        embed.set_footer(text="System operacyjny • Zaproszenie aktywne")
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
            "✅ Seria wysłana. Kliknij ponownie, aby kontynuować:",
            view=RaidControlView(self.text),
            ephemeral=True
        )

class SecretBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = SecretBot()

@bot.tree.command(name="spam", description="Nalot z linkiem (bez powiadomień)")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def spam(interaction: discord.Interaction, wiadomosc: str):
    view = RaidControlView(wiadomosc)
    await interaction.response.send_message("⚙️ **PANEL REKLAMOWY GOTOWY**", view=view, ephemeral=True)

bot.run(TOKEN)
