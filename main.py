import os
import random
from datetime import timedelta
from re import search, sub

import discord
import pymongo
from discord.ext import commands, tasks
from discord.utils import get

from config import *
from util import *

# mongo database
client = pymongo.MongoClient(MONGODB_ATLAS_URI)
db = client['discord-bot']['discord-bot']

# Manage members permission
intents = discord.Intents.default()
intents.members = True

# Bot client
bot = commands.Bot(command_prefix='$', intents=intents)

# Refreshes the sheets' commands and triggers
def refreshBot():
    # Sets use of global variables
    global spreadsheet; global commandSheet; global triggerSheet

    spreadsheet, commandSheet, triggerSheet, isEmpty = refreshSheet()
    refreshCogs(bot, commandSheet)

    return isEmpty

# When the bot has finished loading after being launched
@bot.event
async def on_ready():
    print("\n [*] The bot is running.")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
    print("\n [*] The bot's status was successfully set.")

    periodicRefresh.start()
    print("\n [*] The periodic refresh task was successfully started.")

# Whenever a member joins the server
@bot.event
async def on_member_join(member):
    print(f"\n [*] {member.display_name} has joined the server.")

    # Gets all roles that sould be added to the members
    roles = db.find_one({"description": "onMemberJoinRoles"})['roles']
    roles = list(filter(lambda r: r, map(lambda r: get(member.guild.roles, name=r), roles)))

    # If there are any roles to be added, add them to the member that just joined
    if roles: await member.add_roles(roles if len(roles) > 1 else roles[0])

    # Sends a welcome message at the WELCOME_CHANNEL
    channel = get(member.guild.text_channels, name=WELCOME_CHANNEL)
    response = await channel.send(f'{member.mention} Seja bem vindo(a), meu {random.choice(VOCATIVES)}!')
    print("   [**] The welcome message was successfully sent.")

    await reactToResponse(bot, response)

# Whenever a new message is sent to a channel the bot has access to
@bot.event
async def on_message(message):
    if message.author == bot.user: return

    # Checks for all triggers listed in the spreadsheet
    for element in triggerSheet:
        if message.content and message.content.lower() in [ trigger for trigger in element["TRIGGER"].split('\n') if trigger ]:
            print(f"\n [*] Trigger: '{message.content}', by {message.author.display_name}.")

            await reactToMessage(bot, message, [MESSAGE_EMOJI])

            image_links = element["RESPONSE IMAGE"].split('\n')

            # gets image attatchment
            images = getImages(image_links)

            # activates text-to-speech if specified
            tts = element['TTS'] == 'TRUE'

            # If an image link was specified
            if images:
                response = await message.channel.send(content=element["RESPONSE TEXT"], files=[ discord.File(img) for img in images ], tts=tts)

                # Deletes the image from local directory
                for img in images: os.remove(img)

            else:
                response = await message.channel.send(content=element["RESPONSE TEXT"], tts=tts)

            print("   [**] The response was successfully sent.")

            await reactToResponse(bot, response)

            return

    await bot.process_commands(message)

# Bot's developer
@bot.command(brief='Desenvolvedor do bot e repositório no GitHub.', aliases=['créditos', 'creditos', 'dev'])
async def credits(ctx):
    await ctx.trigger_typing()

    print("\n [*] '>credits' command called.")

    await reactToMessage(bot, ctx.message, ['🤙', '🍉', '😁', '💜', '👋'])

    response = await ctx.reply("Esse bot foi desenvolvido pelo Flip em um momento de tédio. Obrigado pelo interesse <3 \nGitHub: https://github.com/lucasvianav. \nRepositório no GitHub: https://github.com/lucasvianav/discord-chatbot.")
    print("   [**] The response was successfully sent.")
    await reactToResponse(bot, response)

# Calls refreshSheet() (definition in config.py)
@bot.command(brief='Atualiza os comandos a partir da planilha.', aliases=['atualizar', 'update'])
async def refresh(ctx):
    await ctx.trigger_typing()

    print("\n [*] '>refresh' command called.")

    await reactToMessage(bot, ctx.message, ['🔝', '👌', '🆗'])

    isEmpty = refreshBot()

    if not isEmpty:
        print("   [**] The commands and triggers were successfully updated.")
        response = await ctx.send("Os comandos e triggers foram atualizados com sucesso.")
        print("   [**] The response was successfully sent.")
        await reactToResponse(bot, response)

    else:
        print("   [**] There are no commands nor triggers registered.")
        response = await ctx.send("Não há comandos nem triggers cadastrados.")
        print("   [**] The response was successfully sent.")
        await reactToResponse(bot, response, emojiList=['😢'])

# deletes all messages sent by the bot or that triggered it
# (does not delete "important" messages, like from >trackPresence and >openProjects commands)
@bot.command(
    aliases=['clean', 'limpar'],
    brief='Limpa o chat,',
    help='Exclui todas os comandos e mensagens do bot que foram enviadas nos últimos 10 minutos.'
)
async def clear(ctx):
    await ctx.trigger_typing()

    print(f'\n [*] \'>clear\' command called on the {ctx.channel.name} channel.')

    await reactToMessage(bot, ctx.message, ['⚰️'])

    timestamp = ctx.message.created_at - timedelta(minutes=10)

    def filterFunction(m):
        notPinned = not m.pinned
        isMe = (m.author == bot.user)
        isImportant = search(r'`\[ABERTURA DE PROJETOS\]`\n\n', m.content) or search(r'`\[PRESENÇA DE REUNIÃO\]`\n\n', m.content) or search(r'`\[VOTAÇÃO\]`\n\n', m.content)
        # hasPrefix = search('^>\S.*$', m.content)
        didIReact = get(m.reactions, me=True)
        isHelp = m.content == '>help'

        return isHelp or (notPinned and not isImportant and (isMe or didIReact))

    deleted = await ctx.channel.purge(after=timestamp, check=filterFunction)

    response = await ctx.send(f'`{len(deleted)} mensagens foram excluídas.`', delete_after=20)

    await reactToResponse(bot, response)

# Refreshes the sheets' commands and triggers every 15 minutes
@tasks.loop(minutes=15)
async def periodicRefresh():
    print("\n [*] Time for a periodic refresh.")

    isEmpty = refreshBot()

    print("   [**] The commands and triggers were successfully updated", end="")
    print(" - none registered.") if isEmpty else print(".")


if __name__ == '__main__':
    refreshCogs(bot, commandSheet, hasLoaded=False)
    bot.run(DISCORD_TOKEN)
