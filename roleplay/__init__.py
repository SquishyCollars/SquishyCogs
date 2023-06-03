from .roleplay import Roleplay

async def setup(bot):
    n = Roleplay()
    await bot.add_cog(n)