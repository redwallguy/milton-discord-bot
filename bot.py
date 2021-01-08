import discord
from discord.ext import commands
import os

import checks, utils
from cogs.voice import VoiceCog
from cogs.admin import AdminCog
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='+', intents=intents)
checks.master_check(bot)

# Add all cogs
bot.add_cog(VoiceCog(bot))
bot.add_cog(AdminCog(bot))

@bot.event
async def on_command(ctx):
    checks.spam.incrSpam(ctx.author.id)

@bot.event
async def on_ready():
    await utils.generate_token() # Generate milton server token
    
    await checks.creds.sync_gods() # Sync list of gods, mods, and banned 
    await checks.creds.sync_mods()
    await checks.creds.sync_banned()
    while True:
        await asyncio.sleep(5)
        checks.spam.flush() # Flush spam cache every 5 seconds

@bot.command()
async def exit(ctx):
    voice = bot.get_cog("VoiceCog")
    if voice is not None:
        await voice.disconnect_voice()
    await bot.close()

# TODO When deploying on heroku, change logging from file to stderr

bot.run(os.environ.get('DISCORD_TOKEN'))

