import disnake
from disnake.ext import commands


class SlashCommands(commands.Cog):
    """ Set up basic slash commands """

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.slash_command(description="Clear n messages")
    @commands.has_permissions(administrator=True)
    async def wipe(self, inter: disnake.ApplicationCommandInteraction, n: int):
        """ Delete 'n' messages """
        await inter.channel.purge(limit=n)
        await inter.response.send_message(content=f"{n} messages deleted.", ephemeral=True)


def setup(client):
    client.add_cog(SlashCommands(client))
    print(f"> Loaded {__name__}")
