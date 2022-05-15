""" Custom Voice Channels module """

from utils.json_utils import load_json, dump_json
from random import randint

import disnake
from disnake.ext import commands
# Todo: refactor every instance of json interaction to the new format

class CustomVC(commands.Cog):
    """ Lets users create their own customizable voice channels """

    def __init__(self, client):
        self.client = client
        self.json: str = f"data/{__name__}"
        self.channelpath: str = "data/{__name__}-channels"

    class VoiceNotConnected(Exception):
        """ Thrown if the author of a command is not in a custom channel """

        def __init__(self):
            message = "You are not connected to a custom voice channel."
            super().__init__(message)

    class NotCustomChannel(Exception):
        """ Thrown if the channel isn't a custom channel """

        def __init__(self):
            message = "You are not in a custom channel."
            super().__init__(message)

    class NotChannelOwner(Exception):
        """ Thrown if the user isn't the channel owner """

        def __init__(self):
            message = "You do not own this channel."
            super().__init__(message)

    @commands.slash_command(description="Whitelist a user to join your voice channel")
    async def vc_whitelist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member
    ):
        """ Whitelist a user """
        custom_channels = load_json(self.channelpath)

        if inter.author.voice is None:  # check if the user is in a voice channel
            raise self.VoiceNotConnected
        if str(inter.author.voice.channel.id) not in custom_channels[str(inter.guild.id)]:
            raise self.NotCustomChannel
        ownerid = custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]
        if inter.author.id != ownerid:
            raise self.NotChannelOwner

        overwrites = inter.author.voice.channel.overwrites
        overwrites[user] = disnake.PermissionOverwrite(connect=True)
        await inter.author.voice.channel.edit(overwrites=overwrites)
        await inter.response.send_message(
            content=f"{user.display_name} is now whitelisted.",
            ephemeral=True
        )

        if not inter.response.is_done():
            await inter.response.send_message(
                content=f"Failed to whitelist {user.display_name}.",
                ephemeral=True
            )

    @commands.slash_command(description="Blacklist a user from joining your voice channel")
    async def vc_blacklist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member
    ):
        """ Blacklist a user """
        custom_channels = load_json(self.channelpath)

        if inter.author.voice is None:  # check if the user is in a voice channel
            raise self.VoiceNotConnected
        if str(inter.author.voice.channel.id) not in custom_channels[str(inter.guild.id)]:
            raise self.NotCustomChannel
        ownerid = custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]
        if inter.author.id != ownerid:
            raise self.NotChannelOwner

        overwrites = inter.author.voice.channel.overwrites
        overwrites[user] = disnake.PermissionOverwrite(connect=False)
        await inter.author.voice.channel.edit(overwrites=overwrites)
        # check if the blacklisted user is in the owner's channel
        if user.voice is not None and user.voice.channel is inter.author.voice.channel:
            await user.move_to(None)  # kick the blacklisted user
        await inter.response.send_message(
            content=f"{user.display_name} is now blacklisted.",
            ephemeral=True)

        if not inter.response.is_done():
            await inter.response.send_message(
                content=f"Failed to blacklist {user.display_name}.",
                ephemeral=True)

    @commands.slash_command(description="Limit the number of users in a custom voice channel.")
    async def vc_limit(self, inter: disnake.ApplicationCommandInteraction, users: int = 0):
        """ Set a user limit on the custom voice channel """
        custom_channels = load_json(self.channelpath)

        if inter.author.voice is None:  # check if the user is in a voice channel
            raise self.VoiceNotConnected
        if str(inter.author.voice.channel.id) not in custom_channels[str(inter.guild.id)]:
            raise self.NotCustomChannel
        ownerid = custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]
        if inter.author.id != ownerid:
            raise self.NotChannelOwner

        await inter.author.voice.channel.edit(user_limit=users)
        await inter.response.send_message(
            content="Voice channel user limit successfully applied.",
            ephemeral=True
        )

        if not inter.response.is_done():
            await inter.response.send_message(content="Failed to set user limit", ephemeral=True)

    @commands.slash_command(description="Change the name of a custom voice channel.")
    async def vc_rename(self, inter: disnake.ApplicationCommandInteraction, name: str = None):
        """ Rename custom voice channel """
        custom_channels = load_json(self.channelpath)

        if inter.author.voice is None:  # check if the user is in a voice channel
            raise self.VoiceNotConnected
        if str(inter.author.voice.channel.id) not in custom_channels[str(inter.guild.id)]:
            raise self.NotCustomChannel
        ownerid = custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]
        if inter.author.id != ownerid:
            raise self.NotChannelOwner

        if name is None:  # reset name to default
            await inter.author.voice.channel.edit(name=f"{inter.author.display_name}\'s Channel")
        else:  # set name to provided arg
            await inter.author.voice.channel.edit(name=name)
        await inter.response.send_message(content="Channel successfully renamed.", ephemeral=True)

        if not inter.response.is_done():
            await inter.response.send_message(
                content="Failed to rename voice channel.",
                ephemeral=True
            )

    @commands.slash_command(description="Lock custom voice channel")
    async def vc_lock(self, inter: disnake.ApplicationCommandInteraction):
        """ Lock the custom voice channel """
        custom_channels = load_json(self.channelpath)

        if inter.author.voice is None:  # check if the user is in a voice channel
            raise self.VoiceNotConnected
        if str(inter.author.voice.channel.id) not in custom_channels[str(inter.guild.id)]:
            raise self.NotCustomChannel
        ownerid = custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]
        if inter.author.id != ownerid:
            raise self.NotChannelOwner

        await inter.author.voice.channel.set_permissions(
            inter.guild.default_role, connect=False)
        await inter.response.send_message(
            content=f"Locked voice channel \"{inter.author.voice.channel.name}\"", ephemeral=True)

        if not inter.response.is_done():
            await inter.response.send_message(
                content="Failed to lock voice channel.",
                ephemeral=True
            )

    @commands.slash_command(description="Unlocks custom voice channel")
    async def vc_unlock(self, inter: disnake.ApplicationCommandInteraction):
        """ Unlock the custom voice channel """
        custom_channels = load_json(self.channelpath)

        if inter.author.voice is None:  # check if the user is in a voice channel
            raise self.VoiceNotConnected
        if str(inter.author.voice.channel.id) not in custom_channels[str(inter.guild.id)]:
            raise self.NotCustomChannel
        ownerid = custom_channels[str(inter.guild.id)][str(inter.author.voice.channel.id)]
        if inter.author.id != ownerid:
            raise self.NotChannelOwner

        await inter.author.voice.channel.set_permissions(
            inter.guild.default_role, connect=True)
        await inter.response.send_message(
            content=f"Unlocked voice channel \"{inter.author.voice.channel.name}\"",
            ephemeral=True
        )

        if not inter.response.is_done:
            await inter.response.send_message(
                content="Failed to unlock voice channel.",
                ephemeral=True
            )

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        """ Listen for movement between custom voice channels """

        guilds_json = load_json(self.json)

        # Check setup
        if str(member.guild.id) not in guilds_json:
            guilds_json[str(member.guild.id)] = {}
            if guilds_json[str(member.guild.id)]["customvc"]:
                category = await member.guild.create_category_channel(name="Custom Voice Channels")
                channel = await category.create_voice_channel(name="Click to Create")
                guilds_json[str(member.guild.id)]["cat"] = category.id
                guilds_json[str(member.guild.id)]["chan"] = channel.id
                dump_json(self.json, guilds_json)

        channels = load_json(self.channelpath)
        if str(member.guild.id) not in channels:
            channels[member.guild.id] = {}
        dump_json(self.channelpath, channels)

        # Channel creation

        # only create a voice channel if the user was not in one before
        if not before.channel and after.channel:
            # check if the joined channel was the guild's create channel
            if after.channel.id == guilds_json[str(member.guild.id)]["chan"]:
                create_category = await self.client.fetch_channel(
                    guilds_json[str(member.guild.id)]["cat"]
                )
                custom_channel = await create_category.create_voice_channel(
                    name=f"{member.display_name}\'s Channel"
                )
                await member.move_to(custom_channel)  # move the member
                custom_channels = load_json(self.channelpath)
                # dict of dicts
                custom_channels[str(member.guild.id)
                                ][custom_channel.id] = member.id
                dump_json(self.channelpath, custom_channels)

        # Channel deletion
        if before.channel:
            custom_channels = load_json(self.channelpath)
            # check if the before channel was a custom channel
            if str(before.channel.id) in custom_channels[str(member.guild.id)]:
                if before.channel.members == []:  # check if the channel is empty
                    await before.channel.delete(reason="Custom channel empty.")
                    custom_channels[str(member.guild.id)].pop(
                        str(before.channel.id))
                else:
                    # check if the user that left was the owner
                    if member.id == custom_channels[str(member.guild.id)][str(before.channel.id)]:
                        # passes ownership on to a random person
                        new_owner = before.channel.members[randint(
                            0, len(before.channel.members) - 1)]
                        custom_channels[str(member.guild.id)][str(
                            before.channel.id)] = new_owner.id
                        overwrites = before.channel.overwrites
                        overwrites[new_owner] = disnake.PermissionOverwrite(
                            manage_channels=True, create_instant_invite=True, move_members=True)
                        overwrites[member] = disnake.PermissionOverwrite(
                            manage_channels=None, create_instant_invite=None, move_members=None)
                        await before.channel.edit(overwrites=overwrites)
            dump_json(self.channelpath, custom_channels)

    @commands.Cog.listener("on_connect")
    async def on_connect(self):
        """ Check for any channel changes while offline """
        guilds_json = load_json(self.json)
        for guild in self.client.guilds:
            category: disnake.CategoryChannel = None
            channel: disnake.VoiceChannel = None
            if str(guild.id) not in guilds_json:
                guilds_json[str(guild.id)] = {}  # initialize the guild's entry
                for channel in guild.channels:
                    if channel.name == "Click to Create":
                        guilds_json[str(guild.id)]["chan"] = channel.id
                        guilds_json[str(guild.id)]["cat"] = channel.category.id
                if guilds_json[str(guild.id)] == {}:
                    category = await guild.create_category_channel(name="Custom Voice Channels")
                    channel = await category.create_voice_channel(name="Click to Create")
                    guilds_json[str(guild.id)]["cat"] = category.id
                    guilds_json[str(guild.id)]["chan"] = channel.id
                dump_json(self.json, guilds_json)
            elif str(guild.id) in guilds_json:
                str_guild_id = str(guild.id)
                try:
                    category = await guild.fetch_channel(guilds_json[str_guild_id]["cat"])
                except (disnake.HTTPException, disnake.NotFound, disnake.Forbidden):
                    category = await guild.create_category_channel(name="Custom Voice Channels")
                try:
                    channel = await guild.fetch_channel(guilds_json[str_guild_id]["chan"])
                except (disnake.HTTPException, disnake.NotFound, disnake.Forbidden):
                    channel = await category.create_voice_channel(name="Click to Create")
                await channel.move(category=category, beginning=True)
                guilds_json[str(guild.id)]["cat"] = category.id
                guilds_json[str(guild.id)]["chan"] = channel.id
                dump_json(self.json, guilds_json)

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        """ Execute setup for custom voice channels """
        guilds_json = load_json(self.json)
        for guild in self.client.guilds:
            if str(guild.id) not in guilds_json:
                guilds_json[str(guild.id)] = {}
                category = await guild.create_category_channel(name="Custom Voice Channels")
                channel = await category.create_voice_channel(name="Click to Create")
                guilds_json[str(guild.id)]["cat"] = category.id
                guilds_json[str(guild.id)]["chan"] = channel.id
                dump_json(self.json, guilds_json)

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        """ Setup voice channels """
        guilds_json = load_json(self.json)
        if str(guild.id) not in guilds_json:
            guilds_json[str(guild.id)] = {}
            category = await guild.create_category_channel(name="Custom Voice Channels")
            channel = await category.create_voice_channel(name="Click to Create")
            guilds_json[str(guild.id)]["cat"] = category.id
            guilds_json[str(guild.id)]["chan"] = channel.id
            dump_json(self.json, guilds_json)


def setup(client):
    """ Load the extension """
    client.add_cog(CustomVC(client))
    print(f"> Loaded {__name__}")
