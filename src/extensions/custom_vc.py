import disnake
from disnake.ext import commands
from random import randint
import json


def load_json(fp: str) -> dict:
    try:
        with open (f"{fp}.json", "r") as f:
            content = json.load(f)
        return content
    except FileNotFoundError:
        f = open(f"{fp}.json", "a+")
        content = {}
        json.dump(content, f, indent=4)
        f.close()
        return content

def dump_json(fp: str, content: dict) -> None:
    with open(f"{fp}.json", "w") as f:
        json.dump(content, f, indent=4)

class Custom_channel():
  def __init__(self, channel: disnake.VoiceChannel, owner: disnake.Member):
    self.channel : disnake.VoiceChannel = channel
    self.owner : disnake.Member = owner

class Custom_VC(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.guild_channels = {}
    self.setup : Bool = False
    self.custom_channels = []

  @commands.slash_command(description = "Whitelist a user to join your voice channel")
  async def whitelist(self, inter : disnake.ApplicationCommandInteraction, user : disnake.Member):
    """ Whitelist a user """
    if inter.author.voice is not None:
      for custom in self.custom_channels:
        if custom.channel.id == inter.author.voice.channel.id and custom.owner.id == inter.author.id:
          overwrites = inter.author.voice.channel.overwrites
          overwrites[user] = disnake.PermissionOverwrite(connect=True)
          await inter.author.voice.channel.edit(overwrites=overwrites)
          await inter.response.send_message(content=f"{user.display_name} is now whitelisted.", ephemeral=True)
    if not inter.response.is_done():
      await inter.response.send_message(content=f"Failed to whitelist {user.display_name}.", ephemeral=True)

  @commands.slash_command(description = "Blacklist a user from joining your voice channel")
  async def blacklist(self, inter : disnake.ApplicationCommandInteraction, user : disnake.Member):
    """ Blacklist a user """
    if inter.author.voice is not None:
      for custom in self.custom_channels:
        if custom.channel.id == inter.author.voice.channel.id and custom.owner.id == inter.author.id:
          overwrites = inter.author.voice.channel.overwrites
          overwrites[user] = disnake.PermissionOverwrite(connect=False)
          await inter.author.voice.channel.edit(overwrites=overwrites)
          await inter.response.send_message(content=f"{user.display_name} is now blacklisted.", ephemeral=True)
    if not inter.response.is_done():
      await inter.response.send_message(content=f"Failed to blacklist {user.display_name}.", ephemeral=True)

  @commands.slash_command(description = "Limit the number of users in a custom voice channel.")
  async def limit(self, inter : disnake.ApplicationCommandInteraction, users : int = 0):
    """ Set a user limit on the custom voice channel """
    if inter.author.voice is not None:
      for custom in self.custom_channels:
        if custom.channel.id == inter.author.voice.channel.id and custom.owner.id == inter.author.id:
          await inter.author.voice.channel.edit(user_limit=users)
          await inter.response.send_message(content="Voice channel user limit successfully applied.", ephemeral=True)
    if not inter.response.is_done():
      await inter.response.send_message(content="Failed to set user limit", ephemeral=True)

  @commands.slash_command(description="Change the name of a custom voice channel.")
  async def rename(self, inter : disnake.ApplicationCommandInteraction, name : str = None):
    """ Rename custom voice channel """
    if inter.author.voice is not None:
      for custom in self.custom_channels:
        if custom.channel.id == inter.author.voice.channel.id and custom.owner.id == inter.author.id:
          if name is None: # reset name to default
            await inter.author.voice.channel.edit(name = f"{custom.owner.display_name}\'s Voice Channel")
          else: # set name to provided arg
            await inter.author.voice.channel.edit(name=name)
          await inter.response.send_message(content="Channel successfully renamed.", ephemeral=True)
    if not inter.response.is_done():
      await inter.response.send_message(content="Failed to rename voice channel.", ephemeral=True)

  @commands.slash_command(description="Lock custom voice channel")
  async def lock(self, inter : disnake.ApplicationCommandInteraction):
    """ Lock the custom voice channel """
    if inter.author.voice is not None:
      for custom in self.custom_channels:
        if custom.channel.id == inter.author.voice.channel.id and custom.owner.id == inter.author.id:
          await inter.author.voice.channel.set_permissions(
            inter.guild.default_role, connect=False)
          await inter.response.send_message(
            content=
            f"Locked voice channel \"{inter.author.voice.channel.name}\"",
            ephemeral=True)
    if not inter.response.is_done():
      await inter.response.send_message(
        content="Failed to lock voice channel.", ephemeral=True)

  @commands.slash_command(description="Unlocks custom voice channel")
  async def unlock(self, inter : disnake.ApplicationCommandInteraction):
    """ Unlock the custom voice channel """
    if inter.author.voice is not None:
      for custom in self.custom_channels:
        if custom.channel.id == inter.author.voice.channel.id and custom.owner.id == inter.author.id:
          await inter.author.voice.channel.set_permissions(
            inter.guild.default_role, connect=True)
          await inter.response.send_message(content = f"Unlocked voice channel \"{inter.author.voice.channel.name}\"", ephemeral = True)
    if not inter.response.is_done:
      await inter.response.send_message(content = "Failed to unlock voice channel.", ephemeral = True)

  @commands.Cog.listener("on_voice_state_update")
  async def on_voice_state_update(self, member, before, after):
    """ Listen for movement between custom voice channels """
    if not self.setup: # check if setup has been executed (used for when cog is reloaded)
      self.guild_channels = load_json("extensions/guilds")
      for guild in self.client.guilds:
        if guild.id in self.client.guilds:
          if self.guild_channels[guild.id][0] is None or self.guild_channels[guild.id][1] is None:
            self.guild_channels[guild.id][0] = await guild.create_category_channel(name = "Custom Voice Channels")
            self.guild_channels[guild.id][1] = channel = await category.create_voice_channel(name = "Click to Create")
          dump_json("guilds", self.guild_channels)
        else:
          self.guild_channels[guild.id] = [None, None]
          self.guild_channels[guild.id][0] = await guild.create_category_channel(name = "Custom Voice Channels")
          self.guild_channels[guild.id][1] = await self.guild_channels[guild.id][0].create_voice_channel(name = "Click to Create")
      self.setup = True
    if before.channel:
      if len(self.custom_channels) > 0:  #checks if custom channels exist
        for custom in self.custom_channels:
          if before.channel.id == custom.channel.id:
            if before.channel.members == []:  #checks if the channel that was left was a custom channel / still has members
              await custom.channel.delete(reason="Owner left.")
              self.custom_channels.remove(custom)
            else:
              if member.id == custom.owner.id:
                custom.owner = before.channel.members[randint(0,len(before.channel.members) - 1)]  #passes ownership on to a random person
                overwrites = before.channel.overwrites
                overwrites[custom.owner] = disnake.PermissionOverwrite(manage_channels=True, create_instant_invite=True, move_members=True)
                overwrites[member] = disnake.PermissionOverwrite(manage_channels=None, create_instant_invite=None, move_members=None)
                await before.channel.edit(overwrites=overwrites)
    if self.guild_channels[member.guild.id][0] is not None and self.guild_channels[member.guild.id][1] is not None:  #check if setup was successful
      if not before.channel and after.channel:
        if after.channel.id == self.guild_channels[member.guild.id][1].id:
          overwrites = {member : disnake.PermissionOverwrite(manage_channels=True, create_instant_invite=True, move_members=True)}
          custom_channel = await self.guild_channels[member.guild.id][0].create_voice_channel(name = f"{member.display_name}\'s Voice Channel", overwrites=overwrites)
          await member.move_to(custom_channel)
          self.custom_channels.append(Custom_channel(custom_channel, member))

  @commands.Cog.listener("on_ready")
  async def on_ready(self):
    """ Execute setup for custom voice channels """
    self.guild_channels = load_json("extensions/guilds")
    for guild in self.client.guilds:
      if guild.id in self.client.guilds:
        if self.guild_channels[guild.id][0] is None or self.guild_channels[guild.id][1] is None:
          self.guild_channels[guild.id][0] = await guild.create_category_channel(name = "Custom Voice Channels")
          self.guild_channels[guild.id][1] = channel = await category.create_voice_channel(name = "Click to Create")
      else:
        self.guild_channels[guild.id] = [None, None]
        self.guild_channels[guild.id][0] = await guild.create_category_channel(name = "1Custom Voice Channels")
        self.guild_channels[guild.id][1] = await self.guild_channels[guild.id][0].create_voice_channel(name = "Click to Create")
    dump_json("guilds", self.guild_channels)
    self.setup = True
# have json store channel IDs instead of channel object

    # for guild in self.client.guilds:
    #   category : disnake.CategoryChannel = None
    #   channel : disnake.VoiceChannel = None
    #   for channels in guild.channels: # check if setup has already been executed
    #     if channels.name == "Custom Voice Channels":
    #       category = channels
    #     if channels.name == "Click to Create":
    #       channel = channels
    #   if category is None or channel is None: # execute setup
    #     category = await guild.create_category_channel(name = "Custom Voice Channels")
    #     channel = await category.create_voice_channel(name = "Click to Create")
    #   self.guild_channels[guild.id] = [category, channel]
    # self.setup = True


def setup(client):
  client.add_cog(Custom_VC(client))
  print(f"> Loaded {__name__}")
