from redbot.core import commands, app_commands
import polling2, time
from opgg.opgg import OPGG
from opgg.summoner import Summoner
from opgg.params import Region
import discord

class JonisZahnrad(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        polling2.poll(target=time.time, step=30, poll_forever=True, step_function=self.pollStep)
        

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search("BettaZero#EUW", Region.EUW)
        await ctx.send(summoner._name)
        await ctx.send(summoner.recent_game_stats[0])
        last_stats = summoner.recent_game_stats[0].myData.stats
        if (last_stats.death > last_stats.kill):
            ans = "<@460119724102123529> du inter, " + str(last_stats.kill) + "Kills und " + str(last_stats.death) + " Tode?"
            await ctx.send(ans)
    
    @commands.Cog.listener()
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        curr_voice_channel = after.channel
        guild = curr_voice_channel.guild
        new_legacy_text_channel = await guild.create_text_channel(
                name=curr_voice_channel.name.replace("'s ", " "),
                category=curr_voice_channel.category,
                reason="AutoRoom: New legacy text channel needed.",
                # overwrites=perms.overwrites if perms.overwrites else {},
            )

    async def pollStep():
        #Check
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search("Doublelift#NA1")
        print(summoner)

    # Slash command to search for a summoner
    @app_commands.command(description="Search for a summoner")
    async def search(self, interaction: discord.Interaction, summoner_name: str):
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search(summoner_name, Region.EUW)
        await interaction.response.send_message(summoner._name)
        await interaction.response.send_message(summoner.recent_game_stats[0])
        

        

