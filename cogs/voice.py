from discord.ext import commands
import requests
import utils
import discord

class VoiceCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    def is_connected(self, voice_channel):
        return next((client for client in self.bot.voice_clients if client.channel == voice_channel), None) is not None

    async def get_voice_client(self, voice_channel):
        if self.is_connected(voice_channel):
            return next((client for client in self.bot.voice_clients if client.channel == voice_channel), None)
        else:
            return await voice_channel.connect()

    @commands.Cog.listener()
    async def on_ready(self):
        await utils.generate_token()

    @commands.command()
    async def play(self, ctx, clip: str, board: str):
        sound_url = None
        server_json = await utils.clip_get({
            'board': board,
            'name': clip
        })
        sound_url = next((entry.get("sound") for entry in server_json), None)
        vc = await self.get_voice_client(ctx.author.voice.channel)
        vc.play(discord.FFmpegPCMAudio(sound_url), after=lambda e: print('done', e)) # TODO change print to logger, make print statement informative


    # @play.error
    # async def play_error(self, ctx, error):
    #     print(error)
    #     await ctx.send(error)
