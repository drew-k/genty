import disnake
from disnake.ext import commands


class HiddenCommands(commands.Cog):
    """ Set up basic slash commands """

    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @commands.command(description="Load an extension", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, path: str):
        """ Load an extension """
        await ctx.message.delete()
        try:
            self.bot.load_extension(path)
            await ctx.send(content=f"{path} was loaded.", delete_after=10)
        except (commands.NoEntryPointError, commands.ExtensionNotFound):
            await ctx.send(content=f"Could not find an extension with name {path}.", delete_after=10)
        except commands.ExtensionAlreadyLoaded:
            try:
                self.bot.reload_extension(path)
                await ctx.send(content=f"{path} was reloaded.", delete_after=10)
            except commands.ExtensionFailed:
                await ctx.send(content="Something went wrong.", delete_after=10)
        except commands.ExtensionFailed:
            await ctx.send(content="Something went wrong.", delete_after=10)

    @commands.command(description="Unload an extension", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, path: str):
        """ Unload an extension """
        await ctx.message.delete()
        try:
            self.bot.unload_extension(path)
            await ctx.send(content=f"{path} was unloaded.", delete_after=10)
        except commands.ExtensionNotFound:
            await ctx.send(contant=f"Could not find an extension with name {path}.", delete_after=10)
        except commands.ExtensionNotLoaded:
            await ctx.send(content=f"{path} was not loaded.", delete_after=10)

def setup(client):
    client.add_cog(HiddenCommands(client))
    print(f"> Loaded {__name__}")
