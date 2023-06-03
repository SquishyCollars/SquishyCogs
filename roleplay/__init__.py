from .roleplay import Roleplay

    """Add the cog to the bot."""
async def setup(bot):
    await bot.add_cog(Roleplay(bot))