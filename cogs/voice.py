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
        self.board = None

    def is_connected(self, voice_channel):
        """
        Returns if there a client connected to the given voice channel

        Parameters:
        voice_channel (discord.VoiceChannel): Voice channel to check connection to

        Returns:
        bool: If there is a voice client connected to the voice channel

        """
        return next((client for client in self.bot.voice_clients if client.channel == voice_channel), None) is not None

    async def get_voice_client(self, voice_channel):
        """
        Gets the voice client associated with a voice channel

        Parameters:
        voice_channel (discord.VoiceChannel): A voice channel to get client from

        Returns:
        discord.VoiceClient: The voice client associated with the given voice channel. Created if it does not exist already
        """
        if self.is_connected(voice_channel):
            return next((client for client in self.bot.voice_clients if client.channel == voice_channel), None)
        else:
            return await voice_channel.connect()

    async def disconnect_voice(self):
        """
        Disconnects voice client

        Parameters: None

        Returns: None
        """
        voice_client = next((client for client in self.bot.voice_clients), None)
        if (voice_client != None):
            await voice_client.disconnect()

    async def get_clips(self, board):
        """
        Gets clips from board.

        Parameters:
        board (str): Name of board to list clips from

        Returns:
        List[clips]: Clips of board
        """
        return await requests.list_board(board)

    async def get_boards(self):
        """
        Gets all boards.

        Parameters: None

        Returns:
        List[boards]: Boards
        """
        return await utils.board_get({})


    @commands.Cog.listener()
    async def on_ready(self):
        """
        Generates Milton server token on ready
        """
        await utils.generate_token()

    @commands.command(aliases=['sb'])
    async def switch_board(self, ctx, board):
        board_list = await self.get_boards()
        temp_list = [b.get('name') for b in board_list]
        if board in temp_list:
            self.board = board
            await ctx.send("Board switched to " + board + ".")
        else:
            await ctx.send("Board does not exist.")

    @commands.command()
    async def ls(self, ctx, board=None):
        """
        Lists clips of <board> and their aliases.

        If no board is provided, the current board is used.

        Clips are listed in the form:
        'clip': ['alias1', 'alias2', ...]
        """
        if board is None:
            if self.board is None:
                await ctx.send("Please switch to or select a board.")
            else:
                board = self.board
        board_list = await self.get_clips(board)
        formatted_response = "Board: " + board + "\n----------\n"
        for clip in board_list:
            formatted_response += "'" + clip.get('name') + "': " + str(clip.get('aliases')) + "\n"
        await ctx.send(formatted_response)

    @commands.command(aliases=['lb'])
    async def boards(self, ctx):
        """
        Lists all boards.
        """
        board_list = await self.get_boards()
        formatted_response = "Boards\n----------\n"
        for board in board_list:
            formatted_response += board.get('name') + "\n"
        await ctx.send(formatted_response)

    @commands.group()
    async def intro(self, ctx):
        if ctx.invoked_subcommand is None:
            pass # TODO show user's intro
    
    @intro.command(name='set')
    async def set_intro(self, ctx, clip, board):
        pass

    @intro.command(name='delete')
    async def delete_intro(self, ctx):
        pass

    @commands.command()
    async def play(self, ctx, clip: str, board: str):
        """
        Plays <clip> from <board> in voice channel user is currently connected to.

        If user is not connected to a voice channel, this will do nothing.
        """
        sound_url = await requests.get_clip(clip, board)
        vc = await self.get_voice_client(ctx.author.voice.channel)
        if (vc != None):
            vc.play(discord.FFmpegPCMAudio(sound_url), after=lambda e: logger.info('done playing'))

    @commands.command()
    async def leave(self, ctx):
        """
        Disconnects bot from voice.
        """
        await self.disconnect_voice()
