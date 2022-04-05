import disnake
from disnake.ext import commands


class HiddenCommands(commands.Cog):
    """ Set up basic slash commands """

    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @commands.command(description="Load an extension", hidden=True)
    @commands.is_owner()
    async def load(self, inter: disnake.ApplicationCommandInteraction, path: str):
        """ Load an extension """
        try:
            self.bot.load_extension(path)
            await inter.response.send_message(content=f"{path} was loaded.", ephemeral=True)
        except (commands.NoEntryPointError, commands.ExtensionNotFound):
            await inter.response.send_message(content=f"Could not find an extension with name {path}.", ephemeral=True)
        except commands.ExtensionAlreadyLoaded:
            try:
                self.bot.reload_extension(path)
                await inter.response.send_message(content=f"{path} was reloaded.", ephemeral=True)
            except commands.ExtensionFailed:
                await inter.response.send_message(content="Something went wrong.", ephemeral=True)
        except commands.ExtensionFailed:
            await inter.response.send_message(content="Something went wrong.", ephemeral=True)

    @commands.command(description="Unload an extension", hidden=True)
    @commands.is_owner()
    async def unload(self, inter: disnake.ApplicationCommandInteraction, path: str):
        """ Unload an extension """
        try:
            self.bot.unload_extension(path)
            await inter.response.send_message(content=f"{path} was unloaded.", ephemeral=True)
        except commands.ExtensionNotFound:
            await inter.response.send_message(contant=f"Could not find an extension with name {path}.", ephemeral=True)
        except commands.ExtensionNotLoaded:
            await inter.response.send_message(content=f"{path} was not loaded.", ephemeral=True)

def setup(client):
    client.add_cog(HiddenCommands(client))
    print(f"> Loaded {__name__}")
