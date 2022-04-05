import json
from random import randint
import disnake
from disnake.ext import commands


def load_json(file_path: str) -> dict:
    """ Load a json at the given path """
    try:
        with open(f"{file_path}.json", "r") as f:
            content = json.load(f)
        return content
    except FileNotFoundError:
        f = open(f"{file_path}.json", "a+")
        content = {}
        json.dump(content, f, indent=4)
        f.close()
        return content

def dump_json(file_path: str, content: dict) -> None:
    """ Dump the contents into a json at the given path """
    with open(f"{file_path}.json", "w") as f:
        json.dump(content, f, indent=4)


class CustomVC(commands.Cog):
    """ Lets users create their own customizable voice channels """
    def __init__(self, client):
        self.client = client
        self.jsonpath: str = "data/guilds"
        self.channelpath: str = "data/channels"

    @commands.slash_command(description="Whitelist a user to join your voice channel")
    async def vc_whitelist(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
        """ Whitelist a user """
        if inter.author.voice is not None:
            custom_channels = load_json(self.channelpath)
            if str(inter.author.voice.channel.id) in custom_channels[str(inter.guild.id)]:
                if inter.author.id == custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]:
                    overwrites = inter.author.voice.channel.overwrites
                    overwrites[user] = disnake.PermissionOverwrite(connect=True)
                    await inter.author.voice.channel.edit(overwrites=overwrites)
                    await inter.response.send_message(content=f"{user.display_name} is now whitelisted.", ephemeral=True)
        if not inter.response.is_done():
            await inter.response.send_message(content=f"Failed to whitelist {user.display_name}.", ephemeral=True)

    @commands.slash_command(description="Blacklist a user from joining your voice channel")
    async def vc_blacklist(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
        """ Blacklist a user """
        if inter.author.voice is not None:
            custom_channels = load_json(self.channelpath)
            if str(inter.author.voice.channel.id) in custom_channels[str(inter.guild.id)]:
                if inter.author.id == custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]:
                    overwrites = inter.author.voice.channel.overwrites
                    overwrites[user] = disnake.PermissionOverwrite(connect=False)
                    await inter.author.voice.channel.edit(overwrites=overwrites)
                    await inter.response.send_message(content=f"{user.display_name} is now blacklisted.", ephemeral=True)
        if not inter.response.is_done():
            await inter.response.send_message(content=f"Failed to blacklist {user.display_name}.", ephemeral=True)

    @commands.slash_command(description="Limit the number of users in a custom voice channel.")
    async def vc_limit(self, inter: disnake.ApplicationCommandInteraction, users: int = 0):
        """ Set a user limit on the custom voice channel """
        if inter.author.voice is not None:
            custom_channels = load_json(self.channelpath)
            if str(inter.author.voice.channel.id) in custom_channels[str(inter.guild.id)]:
                if inter.author.id == custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]:
                    await inter.author.voice.channel.edit(user_limit=users)
                    await inter.response.send_message(content="Voice channel user limit successfully applied.", ephemeral=True)
        if not inter.response.is_done():
            await inter.response.send_message(content="Failed to set user limit", ephemeral=True)

    @commands.slash_command(description="Change the name of a custom voice channel.")
    async def vc_rename(self, inter: disnake.ApplicationCommandInteraction, name: str = None):
        """ Rename custom voice channel """
        if inter.author.voice is not None:
            custom_channels = load_json(self.channelpath)
            if str(inter.author.voice.channel.id) in custom_channels[str(inter.guild.id)]:
                if inter.author.id == custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]:
                    if name is None:  # reset name to default
                        await inter.author.voice.channel.edit(name=f"{inter.author.display_name}\'s Channel")
                    else:  # set name to provided arg
                        await inter.author.voice.channel.edit(name=name)
                    await inter.response.send_message(content="Channel successfully renamed.", ephemeral=True)
        if not inter.response.is_done():
            await inter.response.send_message(content="Failed to rename voice channel.", ephemeral=True)

    @commands.slash_command(description="Lock custom voice channel")
    async def vc_lock(self, inter: disnake.ApplicationCommandInteraction):
        """ Lock the custom voice channel """
        if inter.author.voice is not None:
            custom_channels = load_json(self.channelpath)
            if str(inter.author.voice.channel.id) in custom_channels[str(inter.guild.id)]:
                if inter.author.id == custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]:
                    await inter.author.voice.channel.set_permissions(
                        inter.guild.default_role, connect=False)
                    await inter.response.send_message(
                        content=f"Locked voice channel \"{inter.author.voice.channel.name}\"",
                        ephemeral=True)
        if not inter.response.is_done():
            await inter.response.send_message(
                content="Failed to lock voice channel.", ephemeral=True)

    @commands.slash_command(description="Unlocks custom voice channel")
    async def vc_unlock(self, inter: disnake.ApplicationCommandInteraction):
        """ Unlock the custom voice channel """
        if inter.author.voice is not None:
            custom_channels = load_json(self.channelpath)
            if str(inter.author.voice.channel.id) in custom_channels[str(inter.guild.id)]:
                if inter.author.id == custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]:
                    await inter.author.voice.channel.set_permissions(
                        inter.guild.default_role, connect=True)
                    await inter.response.send_message(content=f"Unlocked voice channel \"{inter.author.voice.channel.name}\"", ephemeral=True)
        if not inter.response.is_done:
            await inter.response.send_message(content="Failed to unlock voice channel.", ephemeral=True)

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        """ Listen for movement between custom voice channels """

        # Check setup
        guilds_json = load_json(self.jsonpath)
        if str(member.guild.id) not in guilds_json:
            category = await member.guild.create_category_channel(name="Custom Voice Channels")
            channel = await category.create_voice_channel(name="Click to Create")
            guilds_json[member.guild.id] = [category.id, channel.id]
            dump_json(self.jsonpath, guilds_json)

        channels = load_json(self.channelpath)
        if str(member.guild.id) not in channels:
            channels[member.guild.id] = {}
        dump_json(self.channelpath, channels)

        # Channel creation
        if not before.channel and after.channel:  # only create a voice channel if the user was not in one before
            # check if the joined channel was the guild's create channel
            if after.channel.id == guilds_json[str(member.guild.id)][1]:
                create_category = await self.client.fetch_channel(guilds_json[str(member.guild.id)][0])
                custom_channel = await create_category.create_voice_channel(name=f"{member.display_name}\'s Channel")
                await member.move_to(custom_channel)  # move the member
                custom_channels = load_json(self.channelpath)
                custom_channels[str(member.guild.id)][custom_channel.id]=member.id  # dict of dicts
                dump_json(self.channelpath, custom_channels)

        # Channel deletion
        if before.channel:
            custom_channels = load_json(self.channelpath)
            # check if the before channel was a custom channel
            if str(before.channel.id) in custom_channels[str(member.guild.id)]:
                if before.channel.members == []:  # check if the channel is empty
                    await before.channel.delete(reason="Custom channel empty.")
                    custom_channels[str(member.guild.id)].pop(str(before.channel.id))
                else:
                    # check if the user that left was the owner
                    if member.id == custom_channels[str(member.guild.id)][str(before.channel.id)]:
                        # passes ownership on to a random person
                        new_owner=before.channel.members[randint(0, len(before.channel.members) - 1)]
                        custom_channels[str(member.guild.id)][str(before.channel.id)]=new_owner.id
                        overwrites=before.channel.overwrites
                        overwrites[new_owner]=disnake.PermissionOverwrite(manage_channels=True, create_instant_invite=True, move_members=True)
                        overwrites[member]=disnake.PermissionOverwrite(manage_channels=None, create_instant_invite=None, move_members=None)
                        await before.channel.edit(overwrites=overwrites)
            dump_json(self.channelpath, custom_channels)

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        """ Execute setup for custom voice channels """
        guilds_json=load_json(self.jsonpath)
        for guild in self.client.guilds:
            category: disnake.CategoryChannel=None
            channel: disnake.VoiceChannel=None
            if str(guild.id) not in guilds_json:
                category=await guild.create_category_channel(name="Custom Voice Channels")
                channel=await category.create_voice_channel(name="Click to Create")
                guilds_json[guild.id]=[category.id, channel.id]
                dump_json(self.jsonpath, guilds_json)

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        """ Setup voice channels """
        guilds_json = load_json(self.jsonpath)
        if str(guild.id) not in guilds_json:
            category=await guild.create_category_channel(name="Custom Voice Channels")
            channel=await category.create_voice_channel(name="Click to Create")
            guilds_json[guild.id]=[category.id, channel.id]
            dump_json(self.jsonpath, guilds_json)


def setup(client):
    client.add_cog(CustomVC(client))
    print(f"> Loaded {__name__}")
