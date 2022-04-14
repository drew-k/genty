""" Hidden commands module """
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

import disnake
from disnake.ext import commands


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
            await ctx.author.send(
                f"Failed to unload extension \"{path}\": try again without suffix."
            )
            self.logger.warning("Failed to unload extension \"%s\": %s",
                                path, exception, extra={"botname": self.bot.user})

    @commands.command(description="View guilds for client with invites", hidden=True)
    @commands.is_owner()
    async def listguilds(self, ctx):
        await ctx.message.delete()
        guilds_embed = disnake.Embed(
            title=f'{self.bot.user.name } is in {len(self.bot.guilds)} guilds',
            description='\u200b',
            color=disnake.Color.dark_teal(),
            timestamp=datetime.datetime.now()
        )
        guilds_embed.set_thumbnail(url=self.bot.user.avatar.url)
        for guild in self.bot.guilds:
            for channel in guild.channels:
                try:
                    invite_link = await channel.create_invite(
                        max_age=60,
                        temporary=True)
                    break
                except disnake.NotFound:
                    continue
            guilds_embed.add_field(
                name=f'{guild.name}: {len(guild.members)} members',
                value='Guild ID `{}`\nOwner: `{}#{}`\nInvite: {}'.format(
                    guild.id,
                    guild.owner.name,
                    guild.owner.tag,
                    invite_link.url),
                inline=False)
        await ctx.author.send(embed=guilds_embed)


def setup(client):
    client.add_cog(HiddenCommands(client))
    print(f"> Loaded {__name__}")
