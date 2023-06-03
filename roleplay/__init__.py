from .roleplay import Roleplay

def setup(bot):
    n = Roleplay()
    await bot.add_cog(n)