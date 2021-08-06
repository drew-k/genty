import discord
from discord.ext import commands
import os

client = commands.Bot(
    command_prefix = "%",
    help_command=None
)

client.run(os.getenv("TOKEN"))