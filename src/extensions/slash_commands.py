import disnake
from disnake.ext import commands


class SlashCommands(commands.Cog):
    """ Set up basic slash commands """

    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @commands.slash_command(description="Load an extension")
    @commands.is_owner()
    async def load(self, inter: disnake.ApplicationCommandInteraction, path: str):
        """ Load an extension """
        try:
            self.bot.load_extension(path)
            await inter.response.send_message(content=f"{path} was loaded.", ephemeral=True)
        except (commands.NoEntryPointError, commands.ExtensionNotFound):
            await inter.response.send_message(content=f"Could not find an extension with name {path}.", ephemeral=True)
        except commands.ExtensionAlreadyLoaded:
            self.bot.reload_extension(path)
            await inter.response.send_message(content=f"{path} was reloaded.", ephemeral=True)

    @commands.slash_command(description="Unload an extension")
    @commands.is_owner()
    async def unload(self, inter: disnake.ApplicationCommandInteraction, path: str):
        """ Unload an extension """
        try:
            self.bot.unload_extension(path)
            await inter.response.send_message(content=f"{path} was unloaded.", ephemeral=True)
        except (commands.NoEntryPointError, commands.ExtensionNotFound): # I think (?) this won't happen because bot.unload_extension only throws disnake.ext.commands.ExtensionNotLoaded
            await inter.response.send_message(contant=f"Could not find an extension with name {path}.", ephemeral=True)
        except commands.ExtensionNotLoaded:
            await inter.response.send_message(content=f"{path} was not loaded.", ephemeral=True)

    @commands.slash_command(description="Clear n messages")
    @commands.has_permissions(administrator=True)
    async def wipe(self, inter: disnake.ApplicationCommandInteraction, n: int):
        """ Delete 'n' messages """
        await inter.channel.purge(limit=n)
        await inter.response.send_message(content=f"{n} messages deleted.", ephemeral=True)


def setup(client):
    client.add_cog(SlashCommands(client))
    print(f"> Loaded {__name__}")
