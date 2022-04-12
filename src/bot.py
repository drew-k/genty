""" Main bot module """

import os
import logging
from logging.handlers import TimedRotatingFileHandler
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
load_dotenv()  # load the environment variable


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


def get_module_logger(module: str):
    """ Return a logger object in the current module """
    # creates a new log file every night at midnight
    handler = TimedRotatingFileHandler(
        "logs/bot.log", when="midnight", interval=1)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(botname)s - %(levelname)s - %(message)s"))
    logger = logging.getLogger(module)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


class Bot(commands.Bot):
    """ Creates a Bot class """

    def __init__(self):
        super().__init__(
            intents=disnake.Intents().all(),
            sync_commands=True,
            sync_commands_on_cog_unload=True,
            command_prefix='.',
            help_command=None,
        )
        # Set up logging
        self.logger = get_module_logger(__name__)
        self.logger.info("Process started: Bot", extra={"botname": self.user})

    def init_cogs(self, folder: str = "extensions") -> None:
        """ Initialize cogs in provided folder """
        for file in os.listdir(folder):
            if file.endswith(".py"):
                self.load_extension(f"{folder}.{file[:-3]}")
                self.logger.info("Loaded extension: %s", file,
                                 extra={"botname": self.user})

    async def on_ready(self):
        """ Executed when the bot is functional """
        print(Format.green + f"> {self.user} is ready." + Format.reset)
        self.logger.info("Bot ready", extra={"botname": self.user})

    async def on_connect(self):
        """ Executed when the bot makes a connection with discord """
        await update_status(self)
        print(Format.yellow + f"> {self.user} came online." + Format.reset)
        self.logger.info("Bot came online", extra={"botname": self.user})

    async def on_disconnect(self):
        """ Executed when the bot loses connection with discord """
        print(Format.red + f"> {self.user} went offline." + Format.reset)
        self.logger.critical("Bot went offline", extra={"botname": self.user})

    async def on_guild_join(self, guild):
        """ Executed when the bot joins a new guild """
        print(Format.blue + f"> {self.user} joined {guild.name}." + Format.reset)
        self.logger.info("Joined guild: Name=%s Guild ID=%d Owner=%s",
                         guild.name,
                         guild.id,
                         guild.owner.name,
                         extra={"botname": self.user}
                         )
        await update_status(self)

    async def on_guild_remove(self, guild):
        """ Executed when the bot leaves a guild """
        print(Format.blue + f"> {self.user} left {guild.name}." + Format.reset)
        self.logger.info("Left guild: Name=%s Guild ID=%d Owner=%s", guild.name,
                         guild.id, guild.owner.name, extra={"botname": self.user})
        await update_status(self)

    async def on_slash_command_error(
        self,
        interaction: disnake.AppCmdInter,
        exception: commands.CommandError
    ):
        """ Executed when a slash command fails """
        error = (f"> %s attempted to use /%s but the interaction failed.\n\tError: %s",
                 interaction.author,
                 interaction.data.name,
                 exception
                 )
        print(
            Format.red + error + Format.reset)
        self.logger.error("Slash Command Error: User=%s Guild ID=%d Interaction=%s Exception=%s",
                          interaction.author,
                          interaction.guild.id,
                          interaction.data.name,
                          exception,
                          extra={"botname": self.user}
                          )
        await interaction.response.send_message(content=exception, ephemeral=True)


def main():
    """ Starts the bot """
    bot = Bot()
    bot.init_cogs()
    bot.run(os.getenv("TOKEN"))
    bot.logger.critical("Process ended: Bot", extra={"botname": bot.user})


if __name__ == "__main__":
    main()
