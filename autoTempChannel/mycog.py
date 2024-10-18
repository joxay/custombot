from redbot.core import commands
import polling2, time
from opgg.opgg import OPGG
from opgg.summoner import Summoner
from opgg.params import Region

class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        polling2.poll(target=time.time, step=0.5, timeout=6, poll_forever=True, step_function=self.pollStep())
        

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")

    async def pollStep():
        #Check
        opgg_obj = OPGG()

        summoner: Summoner = opgg_obj.search("Doublelift#NA1")
        print(summoner)