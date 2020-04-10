import discord
from redbot.core import commands, Config
from random import randint
import aiohttp
import logging

#thanks to jintaku for this, I have mostly just edited their code a little bit!

log = logging.getLogger("Roleplay")  # Thanks to Sinbad for the example code for logging
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()

if logging.getLogger("red").isEnabledFor(logging.DEBUG):
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
log.addHandler(console)

BaseCog = getattr(commands, "Cog", object)


class Roleplay(BaseCog):
    """Roleplay with gifs"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=842364413)
        default_global = {
            "hugs": [
                "https://img2.gelbooru.com/images/ff/63/ff63a3c4329fda2bf1e9704d4e150fea.gif",
                "https://img2.gelbooru.com/images/2c/e8/2ce81403e0279f1a570711f7472b3abb.gif",
                "https://img2.gelbooru.com/images/e2/05/e205e349535e22c07865913770dcad5f.gif",
                "https://img2.gelbooru.com/images/09/f6/09f63a79f70700abb2593862525ade10.gif",
            ],
            "cuddle": [
                "https://cdn.weeb.sh/images/BkTe8U7v-.gif",
                "https://cdn.weeb.sh/images/SykzL87D-.gif",
            ],
            "kiss": [
                "https://img2.gelbooru.com/images/72/3d/723d7b46a080e459321cb0a46fa4ff84.gif",
                "https://img2.gelbooru.com/images/14/15/141537ae7a372f093e7d6996b16c245b.gif",
            ],
            "slap": [
                "https://cdn.weeb.sh/images/H16aQJFvb.gif",
                "https://img2.gelbooru.com/images/d2/2c/d22c2eedd00914ce38efb46d797be031.gif",
            ],
            "pat": [
                "https://cdn.weeb.sh/images/r180y1Yvb.gif",
                "https://img2.gelbooru.com/images/56/b9/56b9297e70fd0312aba34e7ed1608b27.gif",
            ],
            "lick": [
                "https://media1.tenor.com/images/c4f68fbbec3c96193386e5fcc5429b89/tenor.gif?itemid=13451325",
            ],
            "highfive": [
                "https://media1.tenor.com/images/0ae4995e4eb27e427454526c05b2e3dd/tenor.gif?itemid=12376992",
                "https://media1.tenor.com/images/7b1f06eac73c36721912edcaacddf666/tenor.gif?itemid=10559431",
            ],
            "feed": [
                "https://media1.tenor.com/images/93c4833dbcfd5be9401afbda220066ee/tenor.gif?itemid=11223742",
                "https://imgur.com/v7jsPrv",
            ],
            "tickle": [
                "https://img2.gelbooru.com/images/c4/41/c441cf1fce1fe51420796f6bd0e420e1.gif",
                "https://media1.tenor.com/images/05a64a05e5501be2b1a5a734998ad2b2/tenor.gif?itemid=11379130",
            ],
            "poke": [
                "https://img2.gelbooru.com/images/07/86/078690a58e0b816e8e00cc58e090b499.gif",
                "https://media.tenor.com/images/6b5c1554a6ee9d48ab0392603bab8a8e/tenor.gif",
            ],
            "smug": [
                "https://cdn.nekos.life/v3/sfw/gif/smug/smug_027.gif",
                "https://media1.tenor.com/images/0097fa7f957477f9edc5ff147bb9a5ad/tenor.gif?itemid=12390496",
            ],
            "yeet": [
                "https://cdn.discordapp.com/attachments/698115643328954428/698129009510187026/c0df4f465512347363c30206c679c93f850f7a6c_hq.gif",
                "https://cdn.discordapp.com/attachments/698115643328954428/698130791816757248/OK6W_koKDTOqqqLDbIoPAiaCprQ6TFvgkV91TM25JbM.gif",
                "https://cdn.discordapp.com/attachments/698115643328954428/698130707465240676/tumblr_n57jb9SmxO1tzixowo1_500.gif",
                "https://cdn.discordapp.com/attachments/698115643328954428/698130154706305094/kazuma-throwing-darkness.gif",
                "https://cdn.discordapp.com/attachments/698115643328954428/698129912015355954/loli-throwing-should-be-an-olympic-sport.gif",
                "https://media1.tenor.com/images/999fbb5f7e6600e6343eebb24cc04626/tenor.gif",
                "https://media1.tenor.com/images/b909e525194ec8edb6d370f5f01fcc64/tenor.gif",
                "https://media1.tenor.com/images/541b696027d7142b102b3eebd31a5753/tenor.gif",
            ],
            "nyan": [
                "https://media.tenor.com/images/7ea76e888587b947e1b2e6f09a0e016e/tenor.gif",
                "https://media.tenor.com/images/a21c6e60b2f74e4e2db7e80a3668fc59/tenor.gif",
                "https://media.tenor.com/images/b38fa518b3df44594fdab73a25e9aca0/tenor.gif",
                "https://media.tenor.com/images/f0b0dc7f3824f9863131f7627812c646/tenor.gif",
                "https://cdn.discordapp.com/attachments/365231207065321482/365232759129505823/1f77238736710f3b62526c180c38f1a2.gif",
                "https://cdn.discordapp.com/attachments/365231207065321482/376517834802724875/6aecabc2-70a2-4389-8085-852f026cd16f.gif",
            ]
        }
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx, *, user: discord.Member):
        """Hugs a user!"""

        author = ctx.message.author
        images = await self.config.hugs()
        og = len(images)

        nekos = await self.fetch_nekos_life(ctx, "hug")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)


        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} hugs {user.mention}**"
        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx, *, user: discord.Member):
        """Cuddles a user!"""

        author = ctx.message.author
        images = await self.config.cuddle()
        og = len(images)

        nekos = await self.fetch_nekos_life(ctx, "cuddle")

        images.extend(nekos)
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} cuddles {user.mention}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, *, user: discord.Member):
        """Kiss a user!"""

        author = ctx.message.author
        images = await self.config.kiss()
        og = len(images)

        nekos = await self.fetch_nekos_life(ctx, "kiss")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} kisses {user.mention}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, *, user: discord.Member):
        """Slaps a user!"""

        author = ctx.message.author
        images = await self.config.slap()
        og = len(images)

        nekos = await self.fetch_nekos_life(ctx, "slap")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} slaps {user.mention}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, *, user: discord.Member):
        """Pats a user!"""

        author = ctx.message.author
        images = await self.config.pat()
        og = len(images)

        nekos = await self.fetch_nekos_life(ctx, "pat")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} pats {user.mention}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def lick(self, ctx, *, user: discord.Member):
        """Licks a user!"""

        author = ctx.message.author
        images = await self.config.lick()
        og = len(images)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} licks {user.mention}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx, *, user: discord.Member):
        """Highfives a user!"""

        author = ctx.message.author
        images = await self.config.highfive()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} highfives {user.mention}**"

        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx, *, user: discord.Member):
        """Feeds a user!"""

        author = ctx.message.author
        images = await self.config.feed()
        og = len(images)

        nekos = await self.fetch_nekos_life(ctx, "feed")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} feeds {user.mention}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx, *, user: discord.Member):
        """Tickles a user!"""

        author = ctx.message.author
        images = await self.config.tickle()
        og = len(images)

        nekos = await self.fetch_nekos_life(ctx, "tickle")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} tickles {user.mention}**"

        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx, *, user: discord.Member):
        """Pokes a user!"""

        author = ctx.message.author
        images = await self.config.poke()
        og = len(images)

        nekos = await self.fetch_nekos_life(ctx, "poke")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} pokes {user.mention}**"
        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx):
        """Be smug towards someone!"""

        author = ctx.message.author
        images = await self.config.smug()
        og = len(images)

        smug = await self.fetch_nekos_life(ctx, "smug")
        images.extend(smug)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} is smug**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Made with the help of nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def yeet(self, ctx, *, user: discord.Member):
        """Yeets a user!"""

        author = ctx.message.author
        images = await self.config.yeet()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} Yeets {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def nyan(self, ctx):
        """Nyaaaa~!"""

        author = ctx.message.author
        images = await self.config.nyan()
        og = len(images)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} goes nyaaa!~~♡**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    async def fetch_nekos_life(self, ctx, rp_action):

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.nekos.dev/api/v3/images/sfw/gif/{rp_action}/?count=5") as resp:
                try:
                    content = await resp.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError) as ex:
                    log.debug("Pruned by exception, error below:")
                    log.debug(ex)
                    return []

        if content["data"]["status"]["code"] == 200:
            return content["data"]["response"]["urls"]
