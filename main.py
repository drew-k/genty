import discord
from discord.ext import commands
import os
import json
import random

_id = 873565797887389696

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

@client.command(name="lock", pass_context=True)
async def _lock(ctx):
    with open ("channels.json", "r") as f:
        channels = json.load(f)
    if ctx.author.voice != None and str(ctx.author.voice.channel.id) in channels:
        if channels[str(ctx.author.voice.channel.id)] == ctx.author.id:
            await ctx.author.voice.channel.set_permissions(ctx.guild.default_role, connect=False)

@client.command(name="unlock", pass_context=True)
async def _unlock(ctx):
    with open("channels.json", "r") as f:
        channels = json.load(f)
    if ctx.author.voice != None and str(ctx.author.voice.channel.id) in channels:
        if channels[str(ctx.author.voice.channel.id)] == ctx.author.id:
            await ctx.author.voice.channel.set_permissions(ctx.guild.default_role, connect=True)

@client.event
async def on_voice_state_update(member, before, after):
    custom_channel_category = client.get_channel(873294766916386817)
    # Creates VCs
    if not before.channel and after.channel:
        if after.channel.id == _id:
            new_channel = await member.guild.create_voice_channel(
                name=f"{member.display_name}\'s Channel",
                category=custom_channel_category,
                position = 1)
            await member.move_to(new_channel)
            with open ("channels.json", "r") as f:
                try:
                    channels = json.load(f)
                except:
                    channels = {}
            with open ("channels.json", "w") as f:
                channels[str(new_channel.id)] = member.id
                json.dump(channels, f, indent=4)
    # Deletes VCs
    elif before.channel and not after.channel:
        with open ("channels.json", "r") as f:
            channels = json.load(f)
        with open ("channels.json", "w") as f:
            try:
                if str(before.channel.id) in channels:
                    if before.channel.members == []:
                        await before.channel.delete()
                        channels.pop(str(before.channel.id))
                json.dump(channels, f, indent=4)
            except:
                None

    # Deletes any empty custom VCs
    with open ("channels.json", "r") as f:
        channels = json.load(f)
    for channel in member.guild.channels:
        if channel.type == discord.ChannelType.voice:
            if channel.members == []:
                if str(channel.id) in channels:
                    await channel.delete()
                    channels.pop(str(channel.id))
                    with open("channels.json", "w") as f:
                        json.dump(channels, f, indent=4)

@client.event
async def on_ready():
    f=open("channels.json", "a+")
    f=open("prefixes.json", "a+")
    f.close()
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
