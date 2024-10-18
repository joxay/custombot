from .mycog import JonisZahnrad


async def setup(bot):
    await bot.add_cog(JonisZahnrad(bot))