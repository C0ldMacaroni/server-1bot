"""=============================================================================="""
import asyncio
import discord
from discord.ext import commands
import youtube_dl
from discord_components import *
import datetime
import json
import time
# import os
# from random import choice
from discord.voice_client import VoiceClient

# __________________________________________________________________________________
# Variables
voice_clients = {}

isplaying = False

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}
# __________________________________________________________________________________
# Music Pt 1
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def is_connected(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_connected()


# __________________________________________________________________________________
intents = discord.Intents.default()
intents.members = True
# __________________________________________________________________________________
SERVER = 'Kirby Crib'
# __________________________________________________________________________________
bot = commands.Bot(command_prefix='!', intents=intents)
queue = []
loop = False
"""=============================================================================="""


# OnReady
@bot.event
async def on_ready(amount=10000):
    print('Bot Is Online')
    print('----------------------------------------------')
    await bot.change_presence(activity=discord.Game('God'))
    DiscordComponents(bot)
    # __________________________________________
    # Music Request
    buttons2 = [
        [
            Button(style=ButtonStyle.gray, label='Music Request')
        ]
    ]
    buttons3 = [
        [
            Button(style=ButtonStyle.gray, label='Verify')
        ]
    ]
    buttons4 = [
        [
            Button(style=ButtonStyle.gray, label='Red'),
            Button(style=ButtonStyle.gray, label='Orange'),
            Button(style=ButtonStyle.gray, label='Yellow'),
            Button(style=ButtonStyle.gray, label='Green')
        ],
        [
            Button(style=ButtonStyle.gray, label='Blue'),
            Button(style=ButtonStyle.gray, label='Purple'),
            Button(style=ButtonStyle.gray, label='Pink'),
            Button(style=ButtonStyle.gray, label='Black')
        ]
    ]

    delta2 = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    a = discord.Embed(title=f'𝐕𝐞𝐫𝐢𝐟𝐲', description='Click on the button to get full access to the server.', color=0x2F74C9)
    b = discord.Embed(title=f'𝐌𝐮𝐬𝐢𝐜 𝐑𝐞𝐪𝐮𝐞𝐬𝐭', description='Click on the button to request to play music.', color=0x2F74C9)
    c = discord.Embed(title=f'𝐍𝐚𝐦𝐞 𝐂𝐨𝐥𝐨𝐫', description='Click on the button to choose the color of your name.', color=0x2F74C9)
    n = await bot.get_channel(976888246158123028).send(components=buttons3, embed=a)
    await bot.get_channel(977197359152906250).send(components=buttons2, embed=b)
    await bot.get_channel(977178837400055818).send(components=buttons4, embed=c)

    while n.created_at < delta2:
        res2 = await bot.wait_for('button_click')
        role2 = discord.utils.get(res2.guild.roles, id=977202293369888768)
        role3 = discord.utils.get(res2.guild.roles, id=976888692469809232)

        role4 = discord.utils.get(res2.guild.roles, id=977422137549799464)
        role5 = discord.utils.get(res2.guild.roles, id=977422432925253662)
        role6 = discord.utils.get(res2.guild.roles, id=977422548998434816)
        role7 = discord.utils.get(res2.guild.roles, id=977422580296339456)
        role8 = discord.utils.get(res2.guild.roles, id=977422626484019291)
        role9 = discord.utils.get(res2.guild.roles, id=977422797326397441)
        role10 = discord.utils.get(res2.guild.roles, id=977422946870108203)
        role11 = discord.utils.get(res2.guild.roles, id=977425678163120270)

        if res2.component.label == 'Music Request':
            if not res2.message.author.voice:
                channel = discord.utils.get(bot.get_all_channels(), id=977203351450157067)
                await res2.respond(type=4, content=f"You can play music.\nGo to the <#977203277986938890> channel to request what to play.\nGo to the <#977203351450157067> voice channel to listen to the music.")
                await channel.connect()
                await res2.author.add_roles(role2)
                queue.clear()
                # await res2.move_to(971052519969157170)
                await discord.utils.get(bot.get_all_channels(), id=977203277986938890).purge(limit=amount)
            elif res2.message.author.voice:
                await res2.respond(type=4, content=f'Someone else is playing music. Try again later.')
        elif res2.component.label == 'Verify':
            await res2.author.add_roles(role3)
            await res2.respond(type=4, content=f"You have now access to the server. Please read the {role4.mention}.")
        elif res2.component.label == 'Red':
            await res2.author.add_roles(role4)
            await res2.respond(type=4, content=f"Your name color is now {role4.mention}")
        elif res2.component.label == 'Orange':
            await res2.author.add_roles(role5)
            await res2.respond(type=4, content=f"Your name color is now {role5.mention}")
        elif res2.component.label == 'Yellow':
            await res2.author.add_roles(role6)
            await res2.respond(type=4, content=f"Your name color is now {role6.mention}")
        elif res2.component.label == 'Green':
            await res2.author.add_roles(role7)
            await res2.respond(type=4, content=f"Your name color is now {role7.mention}")
        elif res2.component.label == 'Blue':
            await res2.author.add_roles(role8)
            await res2.respond(type=4, content=f"Your name color is now {role8.mention}")
        elif res2.component.label == 'Purple':
            await res2.author.add_roles(role9)
            await res2.respond(type=4, content=f"Your name color is now {role9.mention}")
        elif res2.component.label == 'Pink':
            await res2.author.add_roles(role10)
            await res2.respond(type=4, content=f"Your name color is now {role10.mention}")
        elif res2.component.label == 'Black':
            await res2.author.add_roles(role11)
            await res2.respond(type=4, content=f"Your name color is now {role11.mention}")
            # if discord.utils.get(res2.guild.roles) in res2.roles:
            #     await discord.utils.get(res2.guild.roles).remove_roles(role6)
        # i = 10
        # while i > 0:
        #     i -= 1
        #     time.sleep(1)
        #     if isplaying == True:
        #         break
        # if isplaying == False:
        #     for member in res2.guild.members:
        #         if discord.utils.get(res2.guild.roles, id=972641306432131082) in member.roles:
        #             print('This person was afk')
        #             await member.remove_roles(discord.utils.get(res2.guild.roles, id=972641306432131082))
        #             await member.move_to(None)
        #             queue.clear()
        #             voice_client = res2.guild.voice_client
        #             await voice_client.disconnect()


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is None and before.channel is not None:
        voice_client = member.guild.voice_client
        role = discord.utils.get(member.guild.roles, id=977202293369888768)
        await member.remove_roles(role)
        try:
            await voice_client.disconnect()
        except:
            pass
        print(member.name + " has left Music VC")


@bot.command()
@commands.has_role("ServerOwner")
async def clear(ctx, amount=10000):
    await ctx.channel.purge(limit=amount)


# __________________________________________________________________________________
# Calculator
buttons1 = [
    [
        Button(style=ButtonStyle.grey, label='1'),
        Button(style=ButtonStyle.grey, label='2'),
        Button(style=ButtonStyle.grey, label='3'),
        Button(style=ButtonStyle.blue, label='×'),
        Button(style=ButtonStyle.red, label='Exit')
    ],
    [
        Button(style=ButtonStyle.grey, label='4'),
        Button(style=ButtonStyle.grey, label='5'),
        Button(style=ButtonStyle.grey, label='6'),
        Button(style=ButtonStyle.blue, label='÷'),
        Button(style=ButtonStyle.red, label='←')
    ],
    [
        Button(style=ButtonStyle.grey, label='7'),
        Button(style=ButtonStyle.grey, label='8'),
        Button(style=ButtonStyle.grey, label='9'),
        Button(style=ButtonStyle.blue, label='+'),
        Button(style=ButtonStyle.red, label='Clear')
    ],
    [
        Button(style=ButtonStyle.grey, label='00'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.blue, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
]


def calculate(exp):
    o = exp.replace('×', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = 'An error occurred.'
    return result


@bot.command(name='calculator', help='This command opens the calculator')
async def calculator(ctx):
    m = await ctx.send(content='Calculator Opened')
    expression = 'None'
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    e = discord.Embed(title=f'{ctx.author.name}\'s calculator | {ctx.author.id}', description=expression,
                      timestamp=delta, color=0x2F74C9)
    await m.edit(components=buttons1, embed=e)
    while m.created_at < delta:
        res = await bot.wait_for('button_click')
        if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[0].timestamp < delta:
            expression = res.message.embeds[0].description
            if expression == 'None' or expression == 'An error occurred.':
                expression = ''
            if res.component.label == 'Exit':
                await res.respond(content='Calculator Closed', type=7)
                break
            elif res.component.label == '←':
                expression = expression[:-1]
            elif res.component.label == 'Clear':
                expression = 'None'
            elif res.component.label == '=':
                expression = calculate(expression)
            else:
                expression += res.component.label
            f = discord.Embed(title=f'{res.author.name}\'s calculator|{res.author.id}', description=expression,
                              timestamp=delta, color=0x2F74C9)
            await res.respond(content='', embed=f, components=buttons1, type=7)


# __________________________________________________________________________________
# Ping
@bot.command()
async def ping(ctx):
    d = discord.Embed(title=f'𝐏𝐢𝐧𝐠', description=f'Your ping: {round(bot.latency * 1000)}ms.', color=0x2F74C9)
    await ctx.send(embed=d)


# __________________________________________________________________________________
# Credits
@bot.command(name='credits', help='This command shows who made the bot')
async def credits(ctx):
    d = discord.Embed(title=f'𝐂𝐫𝐞𝐝𝐢𝐭𝐬', description=f'Made by: `ColdMacaroni`', color=0x2F74C9)
    await ctx.send(embed=d)


# __________________________________________________________________________________
# Music Pt 2
# @bot.command(name='join', help='This command makes the bot join the voice channel')
# @commands.has_role("Music")
# async def join(ctx):
#     if not ctx.message.author.voice:
#         await ctx.send("You are not connected to a voice channel")
#         return
#
#     else:
#         channel = ctx.message.author.voice.channel
#
#     await channel.connect()

@bot.command(name='leave', help='This command makes the bot leave the voice channel')
@commands.has_role("Music")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@bot.command(name='loop', help='This command toggles loop mode')
@commands.has_role("Music")
async def loop_(ctx):
    global loop

    if loop:
        await ctx.send('Loop mode is now `False`')
        loop = False

    else:
        await ctx.send('Loop mode is now `True`')
        loop = True


@bot.command(name='play', help='This command plays music')
@commands.has_role("Music")
async def play(ctx):
    global queue

    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    elif len(queue) == 0:
        await ctx.send('Nothing in your queue! Use `!queue` to add a song')

    else:
        try:
            channel = ctx.message.author.voice.channel
            # emoji = discord.utils.get(bot.emojis, name='loading')
            # await channel.connect()
            # await ctx.send(f'Music is loading <a:loading:972271753411850250>')
        except:
            pass

    server = ctx.message.guild
    voice_channel = server.voice_client
    while queue:
        try:
            while voice_channel.is_playing() or voice_channel.is_paused():
                await asyncio.sleep(2)
                pass

        except AttributeError:
            pass

        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(queue[0], loop=bot.loop)
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                # isplaying=True

                if loop:
                    queue.append(queue[0])

                del (queue[0])

            await ctx.send('**Now playing:** {}'.format(player.title))
        # Queue problem
        except:
            break
        # print(player.duration)
        await asyncio.sleep(player.duration)
        if len(queue) == 0:
            role = discord.utils.get(ctx.message.guild.roles, id=977202293369888768)
            for member in ctx.message.guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
                    await member.move_to(None)
                    voice_client = ctx.message.guild.voice_client
                    try:
                        await voice_client.disconnect()
                    except:
                        pass


# Queue problem
# d = discord.Embed(title=f'𝐌𝐮𝐬𝐢𝐜 𝐑𝐞𝐪𝐮𝐞𝐬𝐭', description='Click on the button to request to play music.', color=0x2F74C9)

@bot.command(name='remove')
async def remove(ctx, number):
    global queue

    try:
        del (queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')

    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')


@bot.command(name='volume', help='This command changes the bots volume')
@commands.has_role("Music")
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("Not connected to a voice channel")

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")


@bot.command(name='pause', help='This command pauses the song')
@commands.has_role("Music")
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()
    # isplaying = False


@bot.command(name='resume', help='This command resumes the song')
@commands.has_role("Music")
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()
    # isplaying = True


@bot.command(name='queue', help='This command adds music into your queue')
@commands.has_role("Music")
async def queue_(ctx, *, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue')
    # i = 10
    # while i > 0:
    #     i -= 1
    #     time.sleep(1)
    #     if isplaying==True:
    #         break
    # role = discord.utils.get(ctx.message.guild.roles, id=972641306432131082)
    # if isplaying==False:
    #     for member in ctx.message.guild.members:
    #         if role in member.roles:
    #             print('This person was afk')
    #             await member.remove_roles(role)
    #             await member.move_to(None)
    #             voice_client = ctx.message.guild.voice_client
    #             await voice_client.disconnect()


@bot.command(name='view', help='This command shows the queue')
@commands.has_role("Music")
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}`')


# __________________________________________________________________________________
# Test
@bot.command()
async def test(ctx):
    d = discord.Embed(title=f'𝐓𝐞𝐬𝐭', description='Test', color=0x2F74C9)
    await ctx.send(embed=d)


# __________________________________________________________________________________
# Help Command Disable
@bot.remove_command('help')
# __________________________________________________________________________________
# Add Reaction Role
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 965309540092481586 or message_id == 966206175907557427:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == '✅':
            role = discord.utils.get(guild.roles, name='View')
        elif payload.emoji.name == '🔴':
            role = discord.utils.get(guild.roles, name='Ferrari Math')
        elif payload.emoji.name == '🟠':
            role = discord.utils.get(guild.roles, name='Spanish')
        elif payload.emoji.name == '🟡':
            role = discord.utils.get(guild.roles, name='Science Mrs. T')
        elif payload.emoji.name == '🟢':
            role = discord.utils.get(guild.roles, name='Chorus Mr. Hayden')
        elif payload.emoji.name == '🔵':
            role = discord.utils.get(guild.roles, name='Social Studies Mrs. Keany')
        elif payload.emoji.name == '🟣':
            role = discord.utils.get(guild.roles, name='Health Mr. Gus')

        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('Role has been given')
            else:
                print('Member not found')
        else:
            print('Role not found')


# __________________________________________________________________________________
# Remove Reaction Role
@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 966206175907557427:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if payload.emoji.name == '🔴':
            role = discord.utils.get(guild.roles, name='Ferrari Math')
        elif payload.emoji.name == '🟠':
            role = discord.utils.get(guild.roles, name='Spanish')
        elif payload.emoji.name == '🟡':
            role = discord.utils.get(guild.roles, name='Science Mrs. T')
        elif payload.emoji.name == '🟢':
            role = discord.utils.get(guild.roles, name='Chorus Mr. Hayden')
        elif payload.emoji.name == '🔵':
            role = discord.utils.get(guild.roles, name='Social Studies Mrs. Keany')
        elif payload.emoji.name == '🟣':
            role = discord.utils.get(guild.roles, name='Health Mr. Gus')

        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print('Role has been removed')
            else:
                print('Member not found')
        else:
            print('Role not found')


# __________________________________________________________________________________
# Level System Pt 1
@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)
    # __________________________________________________________________________________
    # Welcome
    for guild in bot.guilds:
        if guild.name == SERVER:
            for channel in guild.channels:
                if channel.name == '│𝐖𝐞𝐥𝐜𝐨𝐦𝐞':
                    await bot.get_channel(channel.id).send(f'{member.mention} Welcome to our server!')


# __________________________________________________________________________________
# Level System Pt 2
@bot.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await bot.process_commands(message)
    # __________________________________________________________________________________
    # Message Tracker
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel)
    delete_word = ['']
    delete_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z']
    # delete_letter2 = ['!']

    print(f'{username}: {user_message} ({channel})')
    # __________________________________________________________________________________
    # Message Delete
    # if channel:
    #     if any(word in message.content.lower() for word in delete_word):
    #         await message.delete()
    if channel == '│𝐂𝐨𝐮𝐧𝐭𝐢𝐧𝐠':
        if any(word in message.content.lower() for word in delete_letter):
            await message.delete()
    # if channel == '🎵𝐌𝐮𝐬𝐢𝐜🎵':
    #     if any(word in message.content.lower() for word in delete_letter2):
    #         await message.delete()


# __________________________________________________________________________________
# Level System Pt 3
async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('users.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}!')
        users[f'{user.id}']['level'] = lvl_end


@bot.command(name='level', help='This command shows your level')
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')


# __________________________________________________________________________________
# Commands
@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬", description="These are the commands you can use in the server.",
                          color=0x2F74C9)
    embed.set_thumbnail(
        url='https://media.istockphoto.com/vectors/chat-bot-ai-and-customer-service-support-concept-vector-flat-person-vector-id1221348467?k=20&m=1221348467&s=612x612&w=0&h=hp8h8MuGL7Ay-mxkmIKUsk3RY4O69MuiWjznS_7cCBw=')
    embed.add_field(name="𝐔𝐭𝐢𝐥𝐢𝐭𝐲 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:",
                    value="• **!calculator**: This command opens the calculator. \n • **!level**: This command shows your level \n • **!ping**: This command shows your ping. \n • **!commands**: This command shows this message.",
                    inline=False)
    embed.add_field(name="𝐌𝐮𝐬𝐢𝐜 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:",
                    value="• **!queue**: This command adds music into your queue. \n • **!view**: This command shows the queue. \n • **!join**: This command makes the bot join the voice channel. \n • **!leave**: This command makes the bot leave the voice channel. \n • **!play**: This command plays music. \n • **!pause**: This command pauses the song. \n • **!resume**: This command resumes the song. \n • **!volume**: This command changes the bots volume.",
                    inline=False)
    await ctx.send(embed=embed)


# __________________________________________________________________________________
# Bot
TOKEN = 'OTY2MTY4ODI2Nzg4MDczNTQy.G_y3So.4RnHficjbIMVZV-ZWJ0C5HJOC40GX31ZthQqaI'
bot.run(TOKEN)