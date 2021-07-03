import random
from asyncio import sleep
from re import search

import discord
from discord.ext import commands
from discord.utils import get

from util import *


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # list all members that have a role
    @commands.command(
        brief='Lista todos os membros de um cargo.',
        help='Sintaxe: ">members $CARGO"\n\n$CARGO pode ser tanto o nome do cargo (exatamente como está escrito no Discord), quanto a mention. Eu irei retornar a lista de todos os membros que possuem aquele cargo - o "apelido" no servidor e o nome de usuário entre parênteses.\nPor exemplo: ">members Kit Bixo", ou ">members @Kit Bixo"\n\nOBS: Se você quiser que eu retorne a mention dos membros, inclua "$mention" no comando. Por exemplo: ">members Kit Bixo $mention".',
        aliases=['membros', 'whosIn', 'whosin', 'rusin']
    )
    async def members(self, ctx, *argv):
        await ctx.trigger_typing()

        print('\n [*] \'>kick\' command called.')
        await reactToMessage(self.bot, ctx.message, [MESSAGE_EMOJI, '⁉️', 'ℹ️'])

        argv = " ".join(argv)

        mention = False
        if ' $mention' in argv:
            mention = True
            argv = argv.replace(' $mention', '')

        role = get(ctx.guild.roles, name=argv)
        if not role: role = get(ctx.guild.roles, mention=argv)

        if not argv: response = 'É necessário fornecer um cargo ao comando. Em caso de dúvidas, envie `>help members`.'

        elif not role: response = f'Infelizmente o cargo `{argv}` não existe.'

        elif not role.members: response = f'O cargo não possui nenhum membro.'

        else:
            getMemberName = lambda m: f'`{m.nick} ({m.name})`' if m.nick else f'`{m.name}`'
            getMemberMention = lambda m: f'{m.mention}'

            members = ", ".join(map(getMemberMention if mention else getMemberName, role.members))
            roleName = role.mention if mention else f"`{role.name}`"

            response = f'Os {len(role.members)} membros do {roleName} são:\n\n{members}'

        response = await ctx.reply(response)

        await reactToResponse(self.bot, response)

def setup(bot):
    bot.add_cog(Utilities(bot))
