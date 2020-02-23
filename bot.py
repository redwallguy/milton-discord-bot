import discord
from discord.ext import commands
import os, aiohttp

server_token = os.environ.get('MILTON_SERVER_TOKEN')

bot = commands.Bot(command_prefix='+')
webserver_session = None

@bot.event
async def on_ready():
    global webserver_session
    webserver_session = aiohttp.ClientSession()

# This works
# @bot.command()
# async def test(ctx, arg1, arg2):
#     server_msg = "Server not connected"
#     if webserver_session is not None:
#         async with webserver_session.get('http://localhost:8000/users') as resp:
#             server_msg = await resp.json()
#     await ctx.send('Hello there, {} {}. Server message is {}'.format(arg1, arg2, server_msg))
#     await webserver_session.close()
#     await bot.close()

@bot.command()
async def test2(ctx):
    sound_url = None
    if webserver_session is not None:
        async with webserver_session.get('http://localhost:8000/clips') as resp:
            server_json = await resp.json()
            sound_url = server_json[0]['sound']
    vc = await ctx.author.voice.channel.connect()
    vc.play(discord.FFmpegPCMAudio(sound_url), after=lambda e: print('done', e))

bot.run(os.environ.get('DISCORD_TOKEN'))

