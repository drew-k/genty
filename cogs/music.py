import disnake
from disnake.ext import commands
import youtube_dl


class MusicPlayer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Play a YouTube video in a voice channel")
    async def play(self, inter : disnake.ApplicationCommandInteraction, url : str):
        if inter.author.voice is not None:
            pass

def setup(client):
  client.add_cog(MusicPlayer(client))
  print(f"> Loaded {__name__}")
