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

ml = 15 #sets min length for when it stops searching online for gifs

class Roleplay(BaseCog):
    """Roleplay with gifs"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=842364413)
        default_global = {
            "hug": [
                "https://media1.tenor.com/images/18474dc6afa97cef50ad53cf84e37d08/tenor.gif",
                "https://media1.tenor.com/images/6db54c4d6dad5f1f2863d878cfb2d8df/tenor.gif",
                "https://cdn.discordapp.com/attachments/365231207065321482/413007963603599363/xUPGckYDiRSKpt2Q4o.gif",
                "https://tenor.com/view/noragami-kofuku-daikoku-hugging-love-gif-14637016",
                "https://media1.tenor.com/images/daffa3b7992a08767168614178cce7d6/tenor.gif",
                "https://cdn.discordapp.com/attachments/402549927894319105/698152378532102174/0bec930221c5c42cf0820a4fb6a859d5.png",
                "https://media1.tenor.com/images/09005550fb8642d13e544d2045a409c5/tenor.gif",
                "https://media1.tenor.com/images/76445cecfdac1c1756eeeffd67ae4a42/tenor.gif",
                "https://media1.tenor.com/images/b0de026a12e20137a654b5e2e65e2aed/tenor.gif",
                "https://media1.tenor.com/images/40aed63f5bc795ed7a980d0ad5c387f2/tenor.gif",
            ],
            "tuck": [
                "https://media.tenor.com/images/9a91231bcba3bc3c37361a68cd991d13/tenor.gif",
                "https://media.tenor.com/images/2beb7b4596fd14ba0b24e70f3aeae8a0/tenor.gif",
                "https://media1.tenor.com/images/ac21cca8c2e6d7de42d23b69828afa76/tenor.gif",
                "https://media1.tenor.com/images/ae7a8aa8083686ac7bdda751608f5aaf/tenor.gif",
            ],
            "kiss": [
                "https://cdn.discordapp.com/attachments/365231207065321482/407290984758640640/6cddb0f881963edc33a38e66502d8f67.gif",
                "https://media1.tenor.com/images/0f0637c4fabb1baff48a88f35bab4eee/tenor.gif",
                "https://media.tenor.com/images/197df534507bd229ba790e8e1b5f63dc/tenor.gif",
                "https://media.tenor.com/images/b82fdbfc8d45eb9652cf5a3863906cc3/tenor.gif",
            ],
            "slap": [
                "https://media.tenor.com/images/0c9d54efda0d9eda6c8cbafdbac6cf76/tenor.gif",
                "https://media.discordapp.net/attachments/402549927894319105/685115586405072896/image0.gif",
                "https://media1.tenor.com/images/5bc60fa342da31f5aec13faf54813cc1/tenor.gif",
                "https://media1.tenor.com/images/a0ef889b08798078e1180f1baba8274b/tenor.gif",
                "https://cdn.discordapp.com/attachments/698107048092500018/698159693410861056/tenor_5.gif",
                "https://media1.tenor.com/images/42621cf33b44ca6a717d448b1223bccc/tenor.gif?itemid=15696850",
                "https://cdn.discordapp.com/attachments/698107048092500018/698189341029171210/0f6d9273d3b6c0312481be1c86e951fa.gif",
                "https://cdn.discordapp.com/attachments/698107048092500018/698189341469442118/OK6W_koKDTOqqqLDbIoPAgpA1_3h9-GfX-jAgmSf6XE.gif",
                "https://cdn.discordapp.com/attachments/698107048092500018/698193528588861530/tenor_1.gif",
            ],
            "pat": [
                "https://cdn.discordapp.com/attachments/698106187593547797/698122036966326282/tenor_5.gif",
                "https://media.tenor.com/images/7cdb415873e24292b11ab31a339dd552/tenor.gif",
                "https://media1.tenor.com/images/005e8df693c0f59e442b0bf95c22d0f5/tenor.gif",
                "https://cdn.discordapp.com/attachments/365231207065321482/365231814601605130/c741fec81ea5eceb8ebcc7b4dc2bedd5.gif",
                "https://cdn.discordapp.com/attachments/365231207065321482/421773429407088641/2oywl03lcrk01.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/698158825684992030/90c56fd0c24ef9152bba28f01946bee1.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/698158846967021629/ccb857b813847072010d43aa8c85ceb1.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/698159187255099402/tumblr_d63c9507eff0e4406531104ebcc04a81_e80aaef7_640.gif",
                "https://media1.tenor.com/images/f7efdcb10a668d5f7fd1e23355069c7a/tenor.gif",
            ],
            "highfive": [
                "https://media1.tenor.com/images/0ae4995e4eb27e427454526c05b2e3dd/tenor.gif?itemid=12376992",
                "https://media1.tenor.com/images/7b1f06eac73c36721912edcaacddf666/tenor.gif?itemid=10559431",
                "https://cdn.discordapp.com/attachments/698156634370867221/698187437142310952/polnarrfff.gif",
                "https://media1.tenor.com/images/b714d7680f8b49d69b07bc2f1e052e72/tenor.gif",
            ],
            "feed": [
                "https://media1.tenor.com/images/93c4833dbcfd5be9401afbda220066ee/tenor.gif?itemid=11223742",
                "https://imgur.com/v7jsPrv",
            ],
            "tickle": [
                "https://img2.gelbooru.com/images/c4/41/c441cf1fce1fe51420796f6bd0e420e1.gif",
                "https://media1.tenor.com/images/05a64a05e5501be2b1a5a734998ad2b2/tenor.gif",
                "https://media1.tenor.com/images/fcbded4ce66ab01317ee009a1aa44404/tenor.gif",
                "https://media1.tenor.com/images/fea79fed0168efcaf1ddfb14d8af1a6d/tenor.gif",
            ],
            "poke": [
                "https://img2.gelbooru.com/images/07/86/078690a58e0b816e8e00cc58e090b499.gif",
                "https://media1.tenor.com/images/01b264dc057eff2d0ee6869e9ed514c1/tenor.gif",
                "https://media1.tenor.com/images/e8b25e7d069c203ea7f01989f2a0af59/tenor.gif",
                "https://cdn.discordapp.com/attachments/698151030247915590/698194536408809553/HelpfulSimplisticCaudata-small.gif",
                "https://cdn.discordapp.com/attachments/698151030247915590/698195022633369691/f99.gif",
            ],
            "smug": [
                "https://cdn.nekos.life/v3/sfw/gif/smug/smug_027.gif",
                "https://media1.tenor.com/images/0097fa7f957477f9edc5ff147bb9a5ad/tenor.gif",
                "https://i.pinimg.com/originals/6c/22/43/6c2243fcf5eec62d6c43e5078c30b1ca.gif",
                "https://gifimage.net/wp-content/uploads/2017/11/gabriel-dropout-gif-1.gif",
                "https://media1.tenor.com/images/76f7160c04d244a5f34d77d25122344e/tenor.gif",
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
            ],
            "cry": [
                "https://cdn.discordapp.com/attachments/365231207065321482/426455193849167872/p5mr8wEctT1wga4wmo1_540.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698145183031885925/aqua-crying-gif.gif",
                "https://media.tenor.com/images/dca3a60e50f96355e30bf009864cd65c/tenor.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698190593695809616/original.gif",
            ],
            "dropkick": [
                "https://media.tenor.com/images/e736e6f45b407e46719e29bc5c918681/tenor.gif",
                "https://media1.tenor.com/images/9f8bb51d0290543e2e2c5938b21309bf/tenor.gif",
                "https://cdn.discordapp.com/attachments/698107074185265222/698152520316616734/giphy_1.gif",
                "https://cdn.discordapp.com/attachments/698107074185265222/698157855450333224/PhysicalEquatorialBarnswallow-size_restricted.gif",
                "https://media1.tenor.com/images/8acac3c0a044cfe25d95547b05be222c/tenor.gif?itemid=10597667",
            ],
            "blush": [
            "https://media.giphy.com/media/T3Vvyi6SHJtXW/giphy.gif",
            "https://media1.tenor.com/images/cc187b06f246e71b07613e3957d87e00/tenor.gif",
            "https://media1.tenor.com/images/5ea40ca0d6544dbf9c0074542810e149/tenor.gif",
            "https://media1.tenor.com/images/dc917566da214fa3c4e7ddcc58228db9/tenor.gif",
            "https://media.tenor.com/images/e7285221088ae2e76cfff431d0467fdc/tenor.gif",
            ],
        }
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx, *, user: discord.Member):
        """Hugs a user!"""

        author = ctx.message.author
        images = await self.config.hug()
        og = len(images)
        if og < ml:
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
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tuck(self, ctx, *, user: discord.Member):
        """Tuck in a user!"""

        author = ctx.message.author
        images = await self.config.Tuck()
        og = len(images)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} tucks in {user.mention}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, *, user: discord.Member):
        """Kiss a user!"""

        author = ctx.message.author
        images = await self.config.kiss()
        og = len(images)
        if og < ml:
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
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, *, user: discord.Member):
        """Slaps a user!"""

        author = ctx.message.author
        images = await self.config.slap()
        og = len(images)
        if og < ml:
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
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, *, user: discord.Member):
        """Pats a user!"""

        author = ctx.message.author
        images = await self.config.pat()
        og = len(images)
        if og < ml:
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
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
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
        if og < ml:
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
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx, *, user: discord.Member):
        """Tickles a user!"""

        author = ctx.message.author
        images = await self.config.tickle()
        og = len(images)
        if og < ml:
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
        if og < ml:
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
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx):
        """Be smug!"""

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
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def yeet(self, ctx, *, user: discord.Member):
        """yeets a user!"""

        author = ctx.message.author
        images = await self.config.yeet()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} yEets {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def nyan(self, ctx):
        """Go nyaaaa~!"""

        author = ctx.message.author
        images = await self.config.nyan()
        og = len(images)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} goes nyan nyan!~♡**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def cry(self, ctx):
        """Cry D:"""

        author = ctx.message.author
        images = await self.config.cry()
        og = len(images)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} cries**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def dropkick(self, ctx, *, user: discord.Member):
        """Dropkick a user!"""

        author = ctx.message.author
        images = await self.config.dropkick()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} dropkicks {user.mention}**"

        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def blush(self, ctx):
        """Blush"""

        author = ctx.message.author
        images = await self.config.blush()
        og = len(images)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} is blushing**"
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
