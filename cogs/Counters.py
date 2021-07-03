import random
from asyncio import sleep
from re import search

import pymongo
from discord.ext import commands
from discord.utils import get

from config import *
from config import MONGODB_ATLAS_URI
from util import *


class Counters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Database
        client = pymongo.MongoClient(MONGODB_ATLAS_URI)
        self.db = client['discord-bot-vii-rpg']['users']

    @commands.command(brief='', help='', aliases=[])
    async def addNat1(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>addNat1\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        user = user_dice_counter(self.db, ctx.author.id, incNat1=True)

        response = await ctx.reply(f'Você tirou mais um Natural 1? Caramba... Agora você está com `{user.nat1}`.')

        await reactToResponse(self.bot, response, [':one:'])

    @commands.command(brief='', help='', aliases=[])
    async def addNat20(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>addNat20\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        user = user_dice_counter(self.db, ctx.author.id, incNat20=True)

        response = await ctx.reply(f'Você tirou mais um Natural 20? Uau... Agora você está com `{user.nat20}`.')

        await reactToResponse(self.bot, response, [':two:', ':zero:'])

    @commands.command(brief='', help='', aliases=[])
    async def nat1(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>nat1\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        user = user_dice_counter(self.db, ctx.author.id)

        response = await ctx.reply(f'Você está com `{user.nat1}` Natural 1s.')

        await reactToResponse(self.bot, response, [':one:'])

    @commands.command(brief='', help='', aliases=[])
    async def nat20(self, ctx):
        await ctx.trigger_typing()

        print(f'\n [*] \'>nat20\' command called.')

        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI])

        user = user_dice_counter(self.db, ctx.author.id)

        response = await ctx.reply(f'Você está com `{user.nat20}` Natural 20s.')

        await reactToResponse(self.bot, response, [':one:'])

def setup(bot):
    bot.add_cog(Counters(bot))
