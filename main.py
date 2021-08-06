import discord
from discord.ext import commands
import os
import json

def findPrefix(client, message):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(
    command_prefix = "%",
    help_command=None
)

@client.event
async def on_ready():
    print(f"Bot online as {client.user}.")

@client.event
async def on_guild_join(guild):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "%"

    with open ("prefixes.json", "w") as f:
        json.dumps(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open ("prefixes.json", "w") as f:
        json.dumps(prefixes, f, indent=4)

client.run(os.getenv("TOKEN"))
