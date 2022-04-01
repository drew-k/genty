import disnake
from disnake.ext import commands
from datetime import datetime


class SlashCommands(commands.Cog):
  def __init__(self, bot):
    self.bot:commands.Bot = bot

  @commands.slash_command(description="Unload an extension")
  @commands.is_owner()
  async def unload(self, inter: disnake.ApplicationCommandInteraction, path: str):
    """ Unload a cog from the bot """
    try:
      self.bot.unload_extension(path)
      await inter.response.send_message(content=f"{path} was unloaded.", ephemeral=True)
    except:
      await inter.response.send_message(content=f"Extension \"{path}\" not loaded or was not able to be found.", ephemeral=True)

  @commands.slash_command(description="Load an extension")
  @commands.is_owner()
  async def load(self, inter: disnake.ApplicationCommandInteraction, path: str):
    """ Load a cog into the bot """
    try:
      self.bot.load_extension(path)
      await inter.response.send_message(content=f"{path} was loaded.", ephemeral=True)
    except:
     await inter.response.send_message(content=f"Extension \"{path}\" already loaded or was not able to be found.", ephemeral=True)

  @commands.slash_command(description="Reload an extension")
  @commands.is_owner()
  async def reload(self, inter : disnake.ApplicationCommandInteraction, path : str):
    """ Reload a cog into the bot """
    try:
      self.bot.reload_extension(path)
      await inter.response.send_message(content=f"{path} was reloaded.", ephemeral=True)
    except:
      try:
        self.bot.load_extension(path)
        await inter.response.send_message(content=f"{path} was not loaded, but now is.", ephemeral=True)
      except:
        await inter.response.send_message(content=f"{path} was not able to be reloaded.", ephemeral=True)

  @commands.slash_command(description="Clear n messages")
  @commands.has_permissions(administrator=True)
  async def wipe(self, inter: disnake.ApplicationCommandInteraction, n: int):
    """ Deletes 'n' messages from a channel """
    await inter.channel.purge(limit=n)
    await inter.response.send_message(content=f"{n} messages deleted.", ephemeral=True)

def setup(client):
  client.add_cog(SlashCommands(client))
  print(f"> Loaded {__name__}")
