import discord
from discord.ext import commands
import os
from cogs.voice import VoiceCog

bot = commands.Bot(command_prefix='+')

# Add all cogs
bot.add_cog(VoiceCog(bot))

@bot.command()
async def exit(ctx):
    voice = bot.get_cog("VoiceCog")
    if voice is not None:
        await voice.disconnect_voice()
    await bot.close()

# TODO When deploying on heroku, change logging from file to stderr

bot.run(os.environ.get('DISCORD_TOKEN'))

