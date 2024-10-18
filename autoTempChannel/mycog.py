from redbot.core import commands, app_commands
import polling2, time
from opgg.opgg import OPGG
from opgg.summoner import Summoner
from opgg.params import Region

class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        polling2.poll(target=time.time, step=30, poll_forever=True, step_function=self.pollStep)
        

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search("BettaZero#EUW", Region.EUW)
        await ctx.send(summoner._name)
        await ctx.send(summoner.recent_game_stats)
        if (summoner.recent_game_stats[0].kill > summoner.recent_game_stats[0].death):
            ans = "@BettaZero du inter, " + summoner.recent_game_stats[0].kill + "Kills und " + summoner.recent_game_stats[0].death + " Tode?"
            await ctx.send(ans)

    


    async def pollStep():
        #Check
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search("Doublelift#NA1")
        print(summoner)