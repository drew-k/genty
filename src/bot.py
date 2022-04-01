import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv() # load the environment variable


class Format():
  """ Console output format options """
  red = '\033[91m'
  green = '\033[92m'
  yellow = '\033[93m'
  blue = '\033[94m'
  bold = '\033[1m'
  italics = '\033[3m'
  underline = '\033[4m'
  reset = '\033[0m'

class Bot(commands.Bot):
  def __init__(self):
    super().__init__(
      intents=disnake.Intents().all(),
      sync_commands_debug=True,
      sync_permissions=True,
    )
    self.startup_time = datetime.now().replace(microsecond=0) # used in the uptime command

  def init_cogs(self, folder: str) -> None:
      """ Initializes cogs in the provided folder """
      for file in os.listdir(folder):
          if file.endswith(".py"):
              self.load_extension(f"{folder}.{file[:-3]}")

  @commands.slash_command(description="Get the current bot uptime.")
  @commands.is_owner()
  async def uptime(self, inter: disnake.ApplicationCommandInteraction):
      """ Outputs the current uptime of the bot """
      current_time = datetime.now().replace(microsecond=0)
      await inter.response.send_message(content=f"Bot has been online for {current_time-self.startup_time}.", ephemeral=True)

  async def on_ready(self):
    print(Format.green + f"> Bot online as {self.user}." + Format.reset)

  async def on_disconnect(self):
    print(Format.red + f"> {self.user} went offline." + Format.reset)

  async def on_slash_command_error(self, inter: disnake.AppCmdInter, error: commands.CommandError):
    print(Format.red + f"> {inter.author} attempted to use /{inter.data.name} but the interaction failed.\n\tError: {error}" + Format.reset)
    await inter.response.send_message(content=error, ephemeral=True)

def main():
  bot = Bot()
  bot.init_cogs("extensions")
  bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
  main()
