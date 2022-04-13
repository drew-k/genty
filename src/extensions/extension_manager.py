""" Extension manager slash command """

import datetime
import os
from typing import List

import disnake
from disnake.ext import commands


class ExtensionManager(commands.Cog):
    """ Extension Manager """
    def __init__(self, client):
        self.client = client

    class Paginator(disnake.ui.View):
        """ Paginator menu """
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
        async def first_page(self,
                             button: disnake.ui.Button,
                             interaction: disnake.MessageInteraction
                             ):
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
        async def prev_page(self,
                            button: disnake.ui.Button,
                            interaction: disnake.MessageInteraction
                            ):
            """ Moves the pagination to the previous embed """
            self.embed_count -= 1
            embed = self.embeds[self.embed_count]

            self.next_page.disabled = False
            self.last_page.disabled = False
            if self.embed_count == 0:
                self.first_page.disabled = True
                self.prev_page.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

        @disnake.ui.button(emoji="✖️", style=disnake.ButtonStyle.red)
        async def remove(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
            """ Removes the pagination """
            await interaction.response.edit_message(view=None)

        @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.secondary)
        async def next_page(self,
                            button: disnake.ui.Button,
                            interaction: disnake.MessageInteraction
                            ):
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
        async def last_page(self,
                            button: disnake.ui.Button,
                            interaction: disnake.MessageInteraction
                            ):
            """ Moves the pagination to the last embed """
            self.embed_count = len(self.embeds) - 1
            embed = self.embeds[self.embed_count]

            self.first_page.disabled = False
            self.prev_page.disabled = False
            self.next_page.disabled = True
            self.last_page.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @commands.slash_command(
        name="extensions",
        description="Manage extensions",
    )
    @commands.has_permissions(administrator=True)
    async def extension_manager(self, inter: disnake.ApplicationCommandInteraction):
        embeds = []
        for extension in os.listdir("extensions"):
            if extension.endswith(".py"):
                embed = disnake.Embed(
                    color=disnake.Color.from_rgb(253, 213, 181),
                    title="Extension Manager",
                    description="Manage settings for extensions",
                    timestamp=datetime.datetime.now(),
                )
                embed.add_field(
                    name=extension[:-3],
                    value="Enabled",
                )
                embeds.append(embed)
        await inter.send(embed=embeds[0], view=self.Paginator(embeds))


def setup(client):
    client.add_cog(ExtensionManager(client))
    print(f"> Loaded {__name__}")
