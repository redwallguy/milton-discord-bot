import discord
from discord.ext import commands
import os
from cogs.voice import VoiceCog

bot = commands.Bot(command_prefix='+')

# Add all cogs
bot.add_cog(VoiceCog(bot))

bot.run(os.environ.get('DISCORD_TOKEN'))

