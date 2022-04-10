""" Main bot module """

import datetime
from typing import List
import disnake
from disnake.ext import commands


class Help(commands.Cog):
    """ Help command """
    def __init__(self, client):
        self.client = client

    class Menu(disnake.ui.View):
        """ Help paginator """
        def __init__(self, embeds: List[disnake.Embed]):
            super().__init__(timeout=300)
            self.embeds = embeds
            self.embed_count = 0

            self.first_page.disabled = True
            self.prev_page.disabled = True

            # Sets the footer of the embeds with their respective page numbers.
            for i, embed in enumerate(self.embeds):
                embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")

        @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
        async def first_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
            """ Moves the pagination back to the first embed """
            self.embed_count = 0
            embed = self.embeds[self.embed_count]
            embed.set_footer(text=f"Page 1 of {len(self.embeds)}")

            self.first_page.disabled = True
            self.prev_page.disabled = True
            self.next_page.disabled = False
            self.last_page.disabled = False
            await interaction.response.edit_message(embed=embed, view=self)

        @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.secondary)
        async def prev_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
            """ Moves the pagination to the previous embed """
            self.embed_count -= 1
            embed = self.embeds[self.embed_count]

            self.next_page.disabled = False
            self.last_page.disabled = False
            if self.embed_count == 0:
                self.first_page.disabled = True
                self.prev_page.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

        @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.red)
        async def remove(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
            """ Removes the pagination """
            await interaction.response.edit_message(view=None)

        @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.secondary)
        async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
            """ Moves the pagination to the next embed """
            self.embed_count += 1
            embed = self.embeds[self.embed_count]

            self.first_page.disabled = False
            self.prev_page.disabled = False
            if self.embed_count == len(self.embeds) - 1:
                self.next_page.disabled = True
                self.last_page.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

        @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
        async def last_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
            """ Moves the pagination to the last embed """
            self.embed_count = len(self.embeds) - 1
            embed = self.embeds[self.embed_count]

            self.first_page.disabled = False
            self.prev_page.disabled = False
            self.next_page.disabled = True
            self.last_page.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @commands.slash_command(name="help", description="Get additional help")
    async def help_slash_command(self, inter=disnake.ApplicationCommandInteraction, command: str = None):
        """ Displays a paginator help menu """
        embeds = []
        for slash_command in self.client.global_slash_commands:
            embed = disnake.Embed(
                color=disnake.Color.from_rgb(253,213,181),
                title="/" + slash_command.name,
                description = slash_command.description,
                timestamp = datetime.datetime.now(),
                )
            if command == slash_command.name:  # check if there is a specific command requested
                embeds.insert(0, embed)
            else:
                embeds.append(embed)
        await inter.send(embed = embeds[0], view=self.Menu(embeds))

def setup(client):
    """ Load the extension """
    client.add_cog(Help(client))
    print(f"> Loaded {__name__}")