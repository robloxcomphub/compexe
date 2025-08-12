import sys
import types

# Create a dummy VoiceClient class with required class attributes
class DummyVoiceClient:
    warn_nacl = False
    warn_ffmpeg = False
    # Add any other expected class attributes if needed

# Create a dummy VoiceProtocol class (empty)
class DummyVoiceProtocol:
    pass

# Mock discord.voice_client module with these classes
voice_client = types.ModuleType('voice_client')
voice_client.VoiceClient = DummyVoiceClient
voice_client.VoiceProtocol = DummyVoiceProtocol
sys.modules['discord.voice_client'] = voice_client

# Mock discord.player module as empty (discord.py imports it but doesn't access members here)
player = types.ModuleType('player')
sys.modules['discord.player'] = player


import discord
from discord import app_commands
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.none())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Commands synced globally and ready.")

client = MyClient()

@client.tree.command(name="say", description="Repeat your message 60 times with 1-second delay")
@app_commands.describe(text="The text to repeat")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message("Starting to send your message...", ephemeral=True)
    for _ in range(60):
        await interaction.channel.send(text)
        await asyncio.sleep(1)

client.run(TOKEN)
