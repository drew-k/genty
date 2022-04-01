import disnake
from disnake.ext import commands
from datetime import datetime


class Uptime(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.startup_time = datetime.now().replace(microsecond=0) # used in the uptime command

  @commands.slash_command(description="Get the current bot uptime.")
  @commands.is_owner()
  async def uptime(self, inter: disnake.ApplicationCommandInteraction):
    """ Outputs the current uptime of the bot """
    current_time = datetime.now().replace(microsecond=0)
    await inter.response.send_message(content=f"Bot has been online for {current_time-self.startup_time}.", ephemeral=True)


def setup(client):
    client.add_cog(Uptime(client))
    printf(f"> Loaded {__name__}")
