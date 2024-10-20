from redbot.core import commands, app_commands, Config
from opgg.opgg import OPGG
from opgg.summoner import Summoner
from opgg.params import Region
import discord


class JonisZahnrad(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=49846531365243)
        # self.textChannel = {}

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search("BettaZero#EUW", Region.EUW)
        await ctx.send(summoner._name)
        await ctx.send(summoner.recent_game_stats[0])
        last_stats = summoner.recent_game_stats[0].myData.stats
        if last_stats.death > last_stats.kill:
            ans = (
                "<@460119724102123529> du inter, "
                + str(last_stats.kill)
                + "Kills und "
                + str(last_stats.death)
                + " Tode?"
            )
            await ctx.send(ans)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        print(before)
        print(after)
        if after.channel is not None:  # Channel join
            textID: str = await self.config.channel(after.channel).textID()
            if textID is None:  # Gibt noch keinen Channel
                guild = member.guild
                textchannel = await guild.create_text_channel(
                    reason="New temp textchannel needed",
                    name=after.channel.name,
                    category=after.channel.category,
                    overwrites={guild.default_role: discord.PermissionOverwrite(view_channel=False)},
                )
                await self.config.channel(after.channel).textID.set(str(textchannel.id))
            else:  # Es gibt schon einen Channel
                textchannel = guild.get_channel(int(textID))
            await textchannel.set_permissions(
                member,
                reason="User joined channel with temp textchannel",
                view_channel=True,
                read_messages=True,
                send_messages=True,
            )

        if before.channel.id is not after.channel.id:  # Channel leave
            textID = await self.config.channel(before.channel).textID()
            if textID is not None:
                textchannel = guild.get_channel(textID)
                await textchannel.set_permissions(
                    member,
                    reason="User left channel with temp textchannel",
                    view_channel=False,
                    read_messages=False,
                    send_messages=False,
                )
                if len(textchannel.members) == 0:
                    await textchannel.delete()
                    await self.config.channel(before.channel).textID.clear()

    async def pollStep():
        # Check
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search("Doublelift#NA1")
        print(summoner)

    # Slash command to search for a summoner
    @app_commands.command(description="Search for a summoner")
    async def search(self, interaction: discord.Interaction, summoner_name: str):
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search(summoner_name, Region.EUW)
        await interaction.response.send_message(summoner._name)
        # await interaction.response.send_message(summoner.recent_game_stats[0]) # Kann nur eine interaction reagieren
