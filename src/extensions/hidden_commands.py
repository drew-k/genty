import disnake
from disnake.ext import commands


class HiddenCommands(commands.Cog):
    """ Set up hidden prefix commands """

    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @commands.command(description="Load an extension", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, path: str):
        """ Load an extension """
        await ctx.message.delete()
        try:
            self.bot.load_extension(path)
            await ctx.author.send(content=f"{path} was loaded.")
        except (commands.NoEntryPointError, commands.ExtensionNotFound):
            await ctx.author.send(content=f"Could not find an extension with name {path}.")
        except commands.ExtensionAlreadyLoaded:
            try:
                self.bot.reload_extension(path)
                await ctx.author.send(content=f"{path} was reloaded.")
            except commands.ExtensionFailed:
                await ctx.author.send(content="Something went wrong.")
        except commands.ExtensionFailed:
            await ctx.author.send(content="Something went wrong.")

    @commands.command(description="Unload an extension", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, path: str):
        """ Unload an extension """
        await ctx.message.delete()
        try:
            self.bot.unload_extension(path)
            await ctx.author.send(content=f"{path} was unloaded.")
        except commands.ExtensionNotFound:
            await ctx.author.send(contant=f"Could not find an extension with name {path}.")
        except commands.ExtensionNotLoaded:
            await ctx.author.send(content=f"{path} was not loaded.")

def setup(client):
    client.add_cog(HiddenCommands(client))
    print(f"> Loaded {__name__}")
