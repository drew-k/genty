import disnake
from disnake.ext import commands
from disnake.ui import Button
from disnake import ButtonStyle
from random import choice
from extensions.custom_vc import load_json, dump_json
import asyncio

def rps_outcome(self, player: disnake.Member, outcome: str) -> None:
        str_player_id = str(player.id)
        rps_json = load_json(self.jsonpath)
        outcomes = ['wins', 'losses', 'ties']
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
            

class RPS(commands.Cog):
    """ Set up basic slash commands """

    def __init__(self, bot):
        self.bot:commands.Bot = bot
        self.jsonpath = "data/rps"    

    @commands.slash_command(name="rps", brief="Game of rock, paper, scissors.",description="Challenge the bot to a game of rock, paper, scissors.")
    async def rps(self, inter: disnake.ApplicationCommandInteraction, stats: bool = False):
        bot_name = self.bot.user.name
        if stats is True:
            rps_json = load_json(self.jsonpath)
            if str(inter.author.id) not in rps_json:
                await inter.send('You have not played a game of RPS yet.', ephemeral=True)
            elif str(inter.author.id) in rps_json:
                stats_embed = disnake.Embed(
                    title=f'RPS Stats for {inter.author.display_name}',
                    description='\u200b',
                    color=disnake.Color.orange()
                )
                stats_embed.add_field(name='Wins:', value=f'> {rps_json[str(inter.author.id)]["wins"]}')
                stats_embed.add_field(name='Losses:', value=f'> {rps_json[str(inter.author.id)]["losses"]}')
                stats_embed.add_field(name='Ties:', value=f'> {rps_json[str(inter.author.id)]["ties"]}')
                if inter.author.avatar == None:
                    stats_embed.set_thumbnail(url=inter.author.display_avatar.url)
                else:
                    stats_embed.set_thumbnail(url=inter.author.avatar.url)
                stats_embed.set_footer(text=bot_name, icon_url=self.bot.user.avatar.url)
                await inter.send(embed=stats_embed)
        else:   
            choose_weapon = ["Rock","Paper","Scissors"]
            comp = choice(choose_weapon)
            yet = disnake.Embed(title=f"{inter.author.display_name}'s Rock Paper Scissors Game!", description = "> You haven't clicked on any button yet!",color = 0xFFEA00)
            out = disnake.Embed(title=f"{inter.author.display_name}, you didn't make a choice on time!", description = "> **Timed Out!**", color=disnake.Color.red())

            await inter.send(
                embed=yet,
                components=[[
                    Button(style=ButtonStyle.blurple, label='Rock', emoji="\u270A"),
                    Button(style=ButtonStyle.green, label='Paper', emoji='\u270B'),
                    Button(style=ButtonStyle.red, label='Scissors', emoji='\u270C')]
                ],
            )

            def check(res):
                return inter.author == res.user and res.channel == inter.channel

            try:
                res = await self.bot.wait_for("button_click", check=check, timeout=10)
                player = res.component.label
                
                win = disnake.Embed(title=f"{inter.author.display_name}, you won with {player}!", description = f"> **You win!** {bot_name} chose {comp}.", color = 0x00FF00)
                lost = disnake.Embed(title=f"{inter.author.display_name}, you lost with {player}!", description = f"> **You lose!** {bot_name} chose {comp}.", color=disnake.Color.red())
                tie = disnake.Embed(title=f"{inter.author.display_name}, it was a tie!",description = f"> **It was a tie!** You and {bot_name} chose {comp}.", color=0x00FF00)

                if player==comp:
                    await inter.edit_original_message(embed=tie,components=[])
                    outcome = 'ties'
                elif player=="Rock" and comp=="Paper" or player=="Paper" and comp=="Scissors" or player=="Scissors" and comp=="Rock":
                    await inter.edit_original_message(embed=lost,components=[])
                    outcome = 'losses'
                elif player=="Rock" and comp=="Scissors" or player=="Paper" and comp=="Rock" or player=="Scissors" and comp=="Paper":
                    await inter.edit_original_message(embed=win,components=[])
                    outcome = 'wins'
                rps_outcome(self, inter.author, outcome)
                
            except asyncio.TimeoutError:
                await inter.edit_original_message(embed=out,components=[])          
        

def setup(client):
    client.add_cog(RPS(client))
    print(f"> Loaded {__name__}")
