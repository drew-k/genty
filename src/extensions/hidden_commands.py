import logging
from logging.handlers import TimedRotatingFileHandler
import disnake
from disnake.ext import commands


def get_module_logger(module: str):
    """ Return a logger object in the current module """
    handler = TimedRotatingFileHandler(
        "logs/bot.log", when="midnight", interval=1)  # creates a new log file every night at midnight
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(botname)s - %(levelname)s - %(message)s"))
    logger = logging.getLogger(module)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


class HiddenCommands(commands.Cog):
    """ Set up hidden prefix commands """

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.logger = get_module_logger(__name__)
        self.logger.info("Process started: Bot", extra={
                         "botname": self.bot.user})

    @commands.command(description="Load an extension", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, path: str):
        """ Load an extension """
        await ctx.message.delete()
        path = f"extensions.{path}"
        try:
            self.bot.load_extension(path)
            await ctx.author.send(content=f"{path} was loaded.")
            self.logger.info("Loaded extension: \"%s\"", path,
                             extra={"botname": self.bot.user})
        except (commands.NoEntryPointError, commands.ExtensionNotFound) as exception:
            await ctx.author.send(content=f"Could not find an extension with name \"{path}\".")
            self.logger.error("Failed to load extension \"%s\": %s",
                              path, exception, extra={"botname": self.bot.user})
        except commands.ExtensionAlreadyLoaded:
            try:
                self.bot.reload_extension(path)
                await ctx.author.send(content=f"{path} was reloaded.")
                self.logger.info("Reloaded extension:\"%s\"",
                                 path, extra={"botname": self.bot.user})
            except commands.ExtensionFailed as exception:
                await ctx.author.send(content="Something went wrong.")
                self.logger.error("Failed to load extension \"%s\": %s", path, exception, extra={
                                  "botname": self.bot.user})
        except commands.ExtensionFailed as exception:
            await ctx.author.send(content="Something went wrong.")
            self.logger.error("Failed to load extension \"%s\": %s",
                              path, exception, extra={"botname": self.bot.user})
        except ModuleNotFoundError as exception:
            await ctx.author.send(f"Failed to load extension \"{path}\": try again without suffix.")
            self.logger.warning("Failed to load extension \"%s\": %s", path, exception, extra={
                                "botname": self.bot.user})

    @commands.command(description="Unload an extension", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, path: str):
        """ Unload an extension """
        await ctx.message.delete()
        path = f"extensions.{path}"
        try:
            self.bot.unload_extension(path)
            await ctx.author.send(content=f"{path} was unloaded.")
            self.logger.info("Unloaded extension: \"%s\"",
                             path, extra={"botname": self.bot.user})
        except commands.ExtensionNotFound as exception:
            await ctx.author.send(contant=f"Could not find an extension with name \"{path}\".")
            self.logger.error("Failed to unload extension \"%s\": %s",
                              path, exception, extra={"botname": self.bot.user})
        except commands.ExtensionNotLoaded as exception:
            await ctx.author.send(content=f"\"{path}\" was not loaded.")
            self.logger.warning("Failed to unload extension \"%s\": %s",
                                path, exception, extra={"botname": self.bot.user})
        except ModuleNotFoundError as exception:
            await ctx.author.send(f"Failed to unload extension \"{path}\": try again without suffix.")
            self.logger.warning("Failed to unload extension \"%s\": %s",
                                path, exception, extra={"botname": self.bot.user})


def setup(client):
    client.add_cog(HiddenCommands(client))
    print(f"> Loaded {__name__}")
