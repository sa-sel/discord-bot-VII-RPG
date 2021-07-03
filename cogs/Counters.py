import pymongo
from discord.ext import commands

from config import *
from config import MONGODB_ATLAS_URI
from util import *


class Counters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Database
        client = pymongo.MongoClient(MONGODB_ATLAS_URI)
        self.db = client['discord-bot-vii-rpg']['users']

    @commands.command(brief='Adiciona mais um Natural 1 na sua contagem.', help='', aliases=['addnat1', 'add1'])
    async def addNat1(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>addNat1\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        user = user_dice_counter(self.db, ctx.author.id, incNat1=True)

        response = await ctx.reply(f'Você tirou mais um Natural 1? Caramba... Agora você está com `{user["nat1"]}`.')

        await reactToResponse(self.bot, response, [':one:'])

    @commands.command(brief='Adiciona mais um Natural 20 na sua contagem.', help='', aliases=['addnat20', 'add20'])
    async def addNat20(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>addNat20\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        user = user_dice_counter(self.db, ctx.author.id, incNat20=True)

        response = await ctx.reply(f'Você tirou mais um Natural 20? Uau... Agora você está com `{user["nat20"]}`.')

        await reactToResponse(self.bot, response, [':two:', ':zero:'])

    @commands.command(brief='Fala quantos Natural 1s você tirou.', help='', aliases=['natural1', 'nat1s', 'natural1s'])
    async def nat1(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>nat1\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        user = user_dice_counter(self.db, ctx.author.id)

        response = await ctx.reply(f'Você está com `{user["nat1"]}` Natural 1s.')

        await reactToResponse(self.bot, response, [':one:'])

    @commands.command(brief='Fala quantos Natural 20s você tirou.', help='', aliases=['natural20', 'nat20s', 'natural20s'])
    async def nat20(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>nat20\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        user = user_dice_counter(self.db, ctx.author.id)

        response = await ctx.reply(f'Você está com `{user["nat20"]}` Natural 20s.')

        await reactToResponse(self.bot, response, [':one:'])

    @commands.command(brief='Mostra o ranking de Natural 1s e 20s.', help='', aliases=[])
    async def ranking(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>ranking\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        users = [
            {
                "name": (await ctx.guild.fetch_member(user["discord_id"])).display_name,
                "nat1": user["nat1"], "nat20": user["nat20"]
            } for user in self.db.find({})
         ]

        nat1s = sorted(users, key=lambda user: user["nat1"])[0:5]
        nat20s = sorted(users, key=lambda user: user["nat20"])[0:5]

        nat20s = "\n".join([ f'{user["name"]}: {user["nat20"]}' for user in nat20s ])
        nat1s = "\n".join([ f'{user["name"]}: {user["nat1"]}' for user in nat1s ])

        response = await ctx.send(f'As pessoas que tiraram mais Natural 20s foram:\n\n{nat20s}')
        response = await ctx.send(f'As pessoas que tiraram mais Natural 1s foram:\n\n{nat1s}')

        await reactToResponse(self.bot, response, [':trophy:'])


def setup(bot):
    bot.add_cog(Counters(bot))
