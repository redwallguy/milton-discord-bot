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
async def test2(ctx, clip, board):
    sound_url = None
    if webserver_session is not None:
        async with webserver_session.get('http://localhost:8000/clips',
                                        headers={
                                            'Authorization': 'Token ' + server_token
                                        },
                                        params={
                                            'board': board,
                                            'name': clip
                                        }) as resp:
            server_json = await resp.json()
            sound_url = next((entry['sound'] for entry in server_json), None)
    vc = await get_voice_client(ctx.author.voice.channel)
    vc.play(discord.FFmpegPCMAudio(sound_url), after=lambda e: print('done', e)) # TODO change print to logger, make print statement informative

def is_connected(voice_channel):
    return next((client for client in bot.voice_clients if client.channel == voice_channel), None) is not None

async def get_voice_client(voice_channel):
    if is_connected(voice_channel):
        return next((client for client in bot.voice_clients if client.channel == voice_channel), None)
    else:
        return await voice_channel.connect()

bot.run(os.environ.get('DISCORD_TOKEN'))

