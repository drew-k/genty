""" RPS module """
import asyncio
import random

import disnake
from disnake import ButtonStyle
from disnake.ext import commands
from disnake.ui import Button

from extensions.custom_vc import dump_json, load_json

choose_weapon = ["Rock", "Paper", "Scissors"]


def update_stats(self, player: disnake.Member, outcome: str) -> None:
    """ " Update player stats in rps.json"""
    str_player_id = str(player.id)
    rps_json = load_json(self.jsonpath)
    outcomes = ["wins", "losses", "ties"]
    if str_player_id in rps_json:
        for stats in rps_json[str_player_id]:
            if stats == outcome:
                rps_json[str_player_id][outcome] += 1
    else:
        rps_json[str_player_id] = {}
        for stat in outcomes:
            if stat == outcome:
                rps_json[str_player_id][stat] = 1
            else:
                rps_json[str_player_id][stat] = 0
    dump_json(self.jsonpath, rps_json)


def is_draw(player_choice, computer_choice) -> bool:
    """Check if game is a draw"""
    if player_choice == computer_choice:
        return True


def get_comp_choice() -> str:
    """Bot will choose Rock, Paper or Scissors"""
    computer_choice = random.choice(choose_weapon)
    return computer_choice


def player_won(player_choice_str: str, computer_choice_str: str) -> bool:
    """Check to see who won"""
    player_choice = player_choice_str[0].lower()
    computer_choice = computer_choice_str[0].lower()
    if player_choice == "r" and computer_choice == "s":
        outcome = True
    elif player_choice == "s" and computer_choice == "p":
        outcome = True
    elif player_choice == "p" and computer_choice == "r":
        outcome = True
    else:
        outcome = False
    return outcome


async def get_stats(
    self, inter: disnake.ApplicationCommandInteraction, bot_name: str
) -> disnake.Embed:
    """Get the stats of the player using RPS command"""
    rps_json = load_json(self.jsonpath)
    if str(inter.author.id) not in rps_json:
        await inter.send("You have not played a game of RPS yet.", ephemeral=True)
    elif str(inter.author.id) in rps_json:
        stats_embed = disnake.Embed(
            title=f"RPS Stats for {inter.author.display_name}",
            description="\u200b",
            color=disnake.Color.orange(),
        )
        stats_embed.add_field(
            name="Wins:", value=f'> {rps_json[str(inter.author.id)]["wins"]}'
        )
        stats_embed.add_field(
            name="Losses:", value=f'> {rps_json[str(inter.author.id)]["losses"]}'
        )
        stats_embed.add_field(
            name="Ties:", value=f'> {rps_json[str(inter.author.id)]["ties"]}'
        )
        if inter.author.avatar is None:
            stats_embed.set_thumbnail(url=inter.author.display_avatar.url)
        else:
            stats_embed.set_thumbnail(url=inter.author.avatar.url)
        stats_embed.set_footer(text=bot_name, icon_url=self.bot.user.avatar.url)
        return stats_embed


async def rps_game(
    self, inter: disnake.ApplicationCommandInteraction, bot_name: str, is_rematch: bool
) -> None:
    """Function to play the RPS game with the bot"""

    yet = disnake.Embed(
        title=f"{inter.author.display_name}'s Rock Paper Scissors Game!",
        description="> Choose your weapon below!",
        color=0xFFEA00,
    )
    out = disnake.Embed(
        title=f"{inter.author.display_name}, you didn't make a choice on time!",
        description="> **Timed Out!**",
        color=disnake.Color.red(),
    )
    match_components = [
        Button(style=ButtonStyle.blurple, label="Rock", emoji="\u270A"),
        Button(style=ButtonStyle.green, label="Paper", emoji="\u270B"),
        Button(style=ButtonStyle.red, label="Scissors", emoji="\u270C"),
    ]
    if is_rematch is False:
        await inter.send(embed=yet, components=match_components)
    else:
        await inter.edit_original_message(embed=yet, components=match_components)

    def check(res):
        return inter.author == res.user and res.channel == inter.channel

    try:
        res = await self.bot.wait_for("button_click", check=check, timeout=10)
        player_choice = res.component.label
        computer_choice = get_comp_choice()

        win = disnake.Embed(
            title=f"{inter.author.display_name}, you won with {player_choice}!",
            description=f"> **You win!** {bot_name} chose {computer_choice}.",
            color=disnake.Color.green(),
        )
        lost = disnake.Embed(
            title=f"{inter.author.display_name}, you lost with {player_choice}!",
            description=f"> **You lose!** {bot_name} chose {computer_choice}.",
            color=disnake.Color.red(),
        )
        tie = disnake.Embed(
            title=f"{inter.author.display_name}, it was a tie!",
            description=f"> **It was a tie!** You and {bot_name} chose {computer_choice}.",
            color=disnake.Color.yellow(),
        )

        if is_draw(player_choice, computer_choice):
            await res.response.edit_message(embed=tie, components=[])
            outcome = "ties"
        elif player_won(player_choice, computer_choice):
            await res.response.edit_message(embed=win, components=[])
            outcome = "wins"
        else:
            await res.response.edit_message(embed=lost, components=[])
            outcome = "losses"
        update_stats(self, inter.author, outcome)
        await inter.edit_original_message(
            components=[
                Button(style=ButtonStyle.red, label="Rematch"),
                Button(style=ButtonStyle.green, label="Done"),
            ]
        )
    except asyncio.TimeoutError:
        await inter.edit_original_message(embed=out, components=[])


class RPS(commands.Cog):
    """Set up basic slash commands"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.jsonpath = "data/rps"

    @commands.slash_command(
        name="rps",
        brief="Game of rock, paper, scissors.",
        description="Challenge the bot to a game of rock, paper, scissors.",
    )
    async def rps(
        self, inter: disnake.ApplicationCommandInteraction, stats: bool = False
    ):
        bot_name = self.bot.user.name
        if stats is True:
            stats_embed = await get_stats(self, inter, bot_name)
            await inter.send(embed=stats_embed)
        else:
            await rps_game(self, inter, bot_name, False)
        loopclose = 0
        while loopclose == 0:
            try:
                res = disnake.MessageInteraction = await self.bot.wait_for(
                    "button_click",
                    check=lambda i: i.author.id == inter.author.id,
                    timeout=10,
                )
            except asyncio.TimeoutError:
                await inter.edit_original_message(components=[])
            if res.component.label == "Rematch":
                await res.response.defer()
                await rps_game(self, inter, bot_name, True)
            if res.component.label == "Done":
                await res.response.edit_message(components=[])
                loopclose = 1
                break


def setup(client):
    client.add_cog(RPS(client))
    print(f"> Loaded {__name__}")
