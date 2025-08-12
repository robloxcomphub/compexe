import sys
import types

# Patch to remove voice dependencies for Python 3.13+
class DummyVoiceClient:
    warn_nacl = False
    warn_ffmpeg = False

class DummyVoiceProtocol:
    pass

voice_client = types.ModuleType('discord.voice_client')
voice_client.VoiceClient = DummyVoiceClient
voice_client.VoiceProtocol = DummyVoiceProtocol
sys.modules['discord.voice_client'] = voice_client

player = types.ModuleType('discord.player')
sys.modules['discord.player'] = player

import discord
from discord import app_commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Commands synced.")

client = MyClient()

@client.tree.command(name="say", description="Makes the bot say something")
@app_commands.describe(text="The text to say")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text)

client.run(TOKEN)
