import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
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

async def update_status(client: disnake.Client) -> None:
    """ Update the bot's activity """
    activity = disnake.Activity(
        type=disnake.ActivityType.playing,
        name=f"in {len(client.guilds)} guilds",
        )
    await client.change_presence(activity=activity)

class Bot(commands.Bot):
    """ Creates a Bot class """
    def __init__(self):
        super().__init__(
            intents=disnake.Intents().all(),
            sync_commands=True,
            sync_commands_on_cog_unload=True,
            command_prefix='.'
            )

    def init_cogs(self, folder: str) -> None:
        """ Initialize cogs in provided folder """
        for file in os.listdir(folder):
            if file.endswith(".py"):
                self.load_extension(f"extensions.{file[:-3]}")

    async def on_ready(self):
        print(Format.green + f"> {self.user} is ready." + Format.reset)

    async def on_connect(self):
        await update_status(self)
        print(Format.yellow + f"> {self.user} came online." + Format.reset)

    async def on_disconnect(self):
        print(Format.red + f"> {self.user} went offline." + Format.reset)

    async def on_guild_join(self, guild):
        print(Format.blue + f"> {self.user} joined {guild.name}." + Format.reset)
        await update_status(self)

    async def on_guild_remove(self, guild):
        print(Format.blue + f"> {self.user} left {guild.name}." + Format.reset)
        await update_status(self)

    async def on_slash_command_error(self, interaction: disnake.AppCmdInter, exception: commands.CommandError):
        print(Format.red + f"> {interaction.author} attempted to use /{interaction.data.name} but the interaction failed.\n\tError: {exception}" + Format.reset)
        await interaction.response.send_message(content=exception, ephemeral=True)

def main():
    bot = Bot()
    bot.init_cogs("extensions")
    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
