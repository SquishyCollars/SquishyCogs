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
                "https://media.giphy.com/media/QFPoctlgZ5s0E/giphy.gif",
                "https://media.giphy.com/media/143v0Z4767T15e/giphy.gif",
                "https://images-ext-1.discordapp.net/external/mhceLC9YahwiD8Ynh1T69zhiRyF6z0UE4hpuF9O47g8/https/cdn.weeb.sh/images/SJZ-Qy35f.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/699818165655568404/BJwpw_XLM.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698859712040665128/unnamed.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698859649813708830/0314113c8ed42b1faf18adcaff95b05e.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698859205574000640/tenor_19.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698856452990697502/449.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698855441341481021/source.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698855053133348904/377538d76d83ec7d9d2be32870d43f2ac931a412_hq.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698854972045131866/0d18a2a7c78f4dad44fe1498573c206916d808a0r1-444-250_hq.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698854879925502002/FoolishRequiredCaracal-small.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698854832831725638/95384d955807cd6735e63b27b11dd202ae9c202cr1-540-500_00.gif",
                "https://media1.tenor.com/images/1d637775ba77f8b23e73535d31fc540b/tenor.gif?itemid=5062546",
                "https://cdn.discordapp.com/attachments/698106135554555914/698854042096500746/5LYzTBVoS196gvYvw3zjwF_DOOLsMLGVYRxlYm-_HYM.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698853559365664818/tumblr_inline_n998n40b2q1sx8vac540.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698853439152717864/d26c65f2d66be540-merriberri-graphic-arts-services-requests.gif",
                "https://cdn.discordapp.com/attachments/698106135554555914/698853358315765770/OffensiveConstantIndianringneckparakeet-small.gif",
            ],
            "tuck": [
                "https://media.tenor.com/images/9a91231bcba3bc3c37361a68cd991d13/tenor.gif",
                "https://media.tenor.com/images/2beb7b4596fd14ba0b24e70f3aeae8a0/tenor.gif",
                "https://media1.tenor.com/images/ac21cca8c2e6d7de42d23b69828afa76/tenor.gif",
                "https://media1.tenor.com/images/ae7a8aa8083686ac7bdda751608f5aaf/tenor.gif",
                "https://media1.tenor.com/images/f9fec6e0314b874556ac150777b9f76d/tenor.gif?itemid=16591577",
                "https://cdn.discordapp.com/attachments/698106187593547797/698849821850730506/giphy_4.gif",
                "https://media.tenor.com/images/2f968f241e1720230d5db160e41a160a/tenor.gif",
            ],
            "kiss": [
                "https://cdn.discordapp.com/attachments/365231207065321482/407290984758640640/6cddb0f881963edc33a38e66502d8f67.gif",
                "https://media1.tenor.com/images/0f0637c4fabb1baff48a88f35bab4eee/tenor.gif",
                "https://media.tenor.com/images/197df534507bd229ba790e8e1b5f63dc/tenor.gif",
                "https://media.tenor.com/images/b82fdbfc8d45eb9652cf5a3863906cc3/tenor.gif",
                "https://cdn.discordapp.com/attachments/698143309947863121/698855734368010302/NiftyNeglectedAstarte-max-1mb.gif",
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
                "https://cdn.discordapp.com/attachments/698106187593547797/698848148784807977/AppropriatePerfectBeardeddragon-small.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/698849280328204348/AggravatingUnconsciousCardinal-size_restricted.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/698849685804417074/tumblr_d81068e55cef3bfb81ba71573c2906a7_18d1fad3_640.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/698849821850730506/giphy_4.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/699817986940469278/tenor_5.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/699817987221487636/HyxG31ktDb.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/699817988722786304/ryXj1JKDb.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/699817989025038449/rytzGAE0W.gif",
                "https://cdn.discordapp.com/attachments/698106187593547797/699817989725356082/pat_019.gif",

            ],
            "highfive": [
                "https://media1.tenor.com/images/0ae4995e4eb27e427454526c05b2e3dd/tenor.gif?itemid=12376992",
                "https://media1.tenor.com/images/7b1f06eac73c36721912edcaacddf666/tenor.gif?itemid=10559431",
                "https://cdn.discordapp.com/attachments/698156634370867221/698187437142310952/polnarrfff.gif",
                "https://media1.tenor.com/images/b714d7680f8b49d69b07bc2f1e052e72/tenor.gif",
                "https://media1.tenor.com/images/7b1f06eac73c36721912edcaacddf666/tenor.gif",
                "https://media1.tenor.com/images/ce85a2843f52309b85515f56a0a49d06/tenor.gif",
                "https://media1.tenor.com/images/16267f3a34efb42598bd822effaccd11/tenor.gif",
                "https://cdn.discordapp.com/attachments/698156634370867221/698857083331805294/anime-high-five-gif-10.gif",
                "https://cdn.discordapp.com/attachments/698156634370867221/698857787790458890/giphy_7.gif",
                "https://cdn.discordapp.com/attachments/698156634370867221/698858328226267196/source_3.gif",
                "https://cdn.discordapp.com/attachments/698156634370867221/698858575967158323/ActualWarmheartedDungbeetle-small.gif",
                "https://cdn.discordapp.com/attachments/698156634370867221/698859244216385576/haikyu.gif",
                "https://cdn.discordapp.com/attachments/698156634370867221/698860003909697627/tenor_23.gif",
                "https://cdn.discordapp.com/attachments/698156634370867221/698860175754264596/lls.gif",
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
                "https://cdn.discordapp.com/attachments/698152577472266250/698851578769178664/284518131a267b5641cc6f3f9618da18466406e4_hq.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698851609282740304/gucci-gucci.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698851658788241428/vf5RXzqGIWrZu.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698852121239617616/s-cd2b92c9c568f0dd2f41ff4bd92c1b51626c6ff2.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698860201121677332/KXlTf5.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698858127566569472/RemoteOblongAntipodesgreenparakeet-size_restricted.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698858015410880512/86714fe4b8235be518273095b4eacc38.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698856620188499968/d38554c6e23b86c81f8d4a3764b38912.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698855818451484702/fea79fed0168efcaf1ddfb14d8af1a6d.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698855792710778990/tenor_17.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698854885205999716/1547045942_1509884550_Classroom_of_the_Elite.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698854813781196830/5aac5b50738ffad0880965d570a38c1a85f16e92_hq.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698852930287042611/tenor_18.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698852913774198784/tumblr_inline_ow4u7pIhWJ1u544cj_540.gif",
                "https://cdn.discordapp.com/attachments/698152577472266250/698852353402601572/1541204181_tickling.gif",

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
                "https://media1.tenor.com/images/5671f5f05529f161d585d6326076e029/tenor.gif?itemid=5602545",
                "https://cdn.discordapp.com/attachments/698107102740348939/698859310507098257/azu-nyangif2.gif",
                "https://cdn.discordapp.com/attachments/698107102740348939/698859849139879986/ThoseRectangularAmoeba-size_restricted.gif",
            ],
            "cry": [
                "https://cdn.discordapp.com/attachments/365231207065321482/426455193849167872/p5mr8wEctT1wga4wmo1_540.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698145183031885925/aqua-crying-gif.gif",
                "https://media.tenor.com/images/dca3a60e50f96355e30bf009864cd65c/tenor.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698190593695809616/original.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698859824032645150/source_1.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698858685740613643/anime-cry-gif-28.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698858454235873290/tenor_22.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698858301525458944/tenor_20.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698855963813478470/1510234964_shelooksbetterwithhairdown.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698855654663651368/tenor_21.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698855632425582612/Anime-Crying-Gif.gif",
                "https://cdn.discordapp.com/attachments/698115673896779776/698855632480239626/4b5e9867209d7b1712607958e01a80f1.gif",
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
            "stinky": [
            "https://media1.tenor.com/images/01c688073bd76808d1190988d2786fdf/tenor.gif?itemid=16154821",
            "https://media1.tenor.com/images/3472cea80508bb61cf4a43b32c7dee56/tenor.gif?itemid=4550346",
            "https://media1.tenor.com/images/a1059f2abf295e91f58cfb287cd101b5/tenor.gif?itemid=15325836",
            "https://media1.tenor.com/images/b0c14e7907748af4f143581aedc4c305/tenor.gif?itemid=7705307",
            "https://media1.tenor.com/images/4eea4b2803caa8858827c45e7778611e/tenor.gif?itemid=3671501",
            "https://media1.tenor.com/images/07302a16845ccb82af069aa86e7567f2/tenor.gif?itemid=16211298",
            "https://media1.tenor.com/images/221c0c243710a9fb197c8fa42918290b/tenor.gif?itemid=12447230",
            ],
            "bonk": [
            "https://cdn.discordapp.com/attachments/698842613226143754/698969166882930738/3vyvfr.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698855735613849630/PzVCgJ.gif",
            "https://media1.tenor.com/images/bc8d9395166b82df05d590459f184f2d/tenor.gif?itemid=16061390",
            "https://cdn.discordapp.com/attachments/698842613226143754/698849968005447800/tenor_12.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698849576991457280/tenor_13.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698849065953263666/atoz.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698848791679467540/tenor_10.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698848725644345464/tenor_9.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698848622715994162/original.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698848418168176650/tenor_15.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698848591942385714/tenor_11.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698848132288610351/8b17798341ae6119f33495da1c8400c6af542515cef4ffce81afb82fe72ddc5c.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698847860988575834/giphy_3.gif",
            "https://cdn.discordapp.com/attachments/698842613226143754/698847645992484884/tenor_14.gif",
            "https://cdn.discordapp.com/attachments/682226699114512429/698838106652278794/20200412_031239.jpg",
            "https://cdn.discordapp.com/emojis/615242366491820071.gif",
            ],
        }
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx, *, text: str = "" ):
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
        embed.description = f"**{author.mention} hugs {text}**"
        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tuck(self, ctx, *, text: str = ""):
        """Tuck in a user!"""

        author = ctx.message.author
        images = await self.config.tuck()
        og = len(images)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} tucks in {text}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, *,text: str = "" ):
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
        embed.description = f"**{author.mention} kisses {text}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, *,text: str = "" ):
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
        embed.description = f"**{author.mention} slaps {text}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, *,text: str = "" ):
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
        embed.description = f"**{author.mention} pats {text}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx, *,text: str = "" ):
        """Highfives a user!"""

        author = ctx.message.author
        images = await self.config.highfive()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} highfives {text}**"

        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx, *,text: str = "" ):
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
        embed.description = f"**{author.mention} feeds {text}**"

        embed.set_image(url=images[i])
        #gives credit when using nekos
        if og < i:
            embed.set_footer(text="Image gotten from nekos.life. Ask quashera how you can help add more custom ones!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx, *,text: str = "" ):
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
        embed.description = f"**{author.mention} tickles {text}**"

        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx, *,text: str = "" ):
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
        embed.description = f"**{author.mention} pokes {text}**"
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
    async def yeet(self, ctx, *,text: str = "" ):
        """yeets a user!"""

        author = ctx.message.author
        images = await self.config.yeet()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} yeets {text}**"
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
    async def dropkick(self, ctx, *,text: str = "" ):
        """Dropkick a user!"""

        author = ctx.message.author
        images = await self.config.dropkick()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} dropkicks {text}**"

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

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def stinky(self, ctx, *,text: str = "" ):
        """Call out a user for being a big stinky"""

        author = ctx.message.author
        images = await self.config.stinky()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        if text  == "":
            embed.description = f"**Uh oh, {author.mention} is stinky!**"
        else:
            embed.description = f"**Uh oh, {author.mention} thinks {text} is a stinky!**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bonk(self, ctx, *,text: str = "" ):
        """bonk someone"""

        author = ctx.message.author
        images = await self.config.bonk()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        if text  == "":
            embed.description = f"**{author.mention} bonks themselves!**"
        else:
            embed.description = f"**{author.mention} bonks {text}**"
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
