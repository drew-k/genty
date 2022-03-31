import disnake
from disnake.ext import commands
import youtube_dl

class MusicPlayer(commands.Cog):
  def __init__(self, client):
    self.client = client

def setup(client):
  client.add_cog(MusicPlayer(client))
  print(f"> Loaded {__name__}")