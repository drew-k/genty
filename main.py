import discord
from discord.ext import commands
import os
import json
import random

def findPrefix(client, message):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(
    command_prefix = (findPrefix),
    help_command=None
)

@client.command(name="help", pass_context=True)
async def _help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title = "Help",
        description = "test",
        color = discord.Color.blue()
    )
    await ctx.author.send(embed=embed)

@client.event
async def on_ready():
    f=open("prefixes.json", "a+")
    print(f"Bot online as {client.user}.")

@client.event
async def on_guild_join(guild):
    with open ("prefixes.json", "r") as f:
        try:
            prefixes = json.load(f)
        except:
            prefixes = {}

    prefixes[str(guild.id)] = "%"

    with open ("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open ("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("say hi"):
        if random.randint(0,3) > 0:
            await message.channel.send("hi")
        else:
            await message.channel.send("leave me alone")

    await client.process_commands(message)

client.run(os.getenv("TOKEN"))
