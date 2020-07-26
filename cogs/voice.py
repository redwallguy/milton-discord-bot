from discord.ext import commands
import requests
import utils
import discord
import logging

logging.basicConfig(filename='milton.log',level=logging.INFO)
logger = logging.getLogger(__name__)

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

    async def disconnect_voice(self):
        voice_client = next((client for client in self.bot.voice_clients), None)
        if (voice_client != None):
            await voice_client.disconnect()

    @commands.Cog.listener()
    async def on_ready(self):
        await utils.generate_token()

    @commands.command()
    async def play(self, ctx, clip: str, board: str):
        sound_url = await requests.get_clip(clip, board)
        logger.info("Sound url " + sound_url)
        vc = await self.get_voice_client(ctx.author.voice.channel)
        vc.play(discord.FFmpegPCMAudio(sound_url), after=lambda e: logger.info('done'))

    @commands.command()
    async def leave(self, ctx):
        await self.disconnect_voice()

    @play.error
    async def play_error(self, ctx, error):
        logger.info(error)
