from discord.ext import commands
import requests
import utils
import discord
import logging, os
import checks

if (os.environ.get("LOGGING_MODE") == 'file'):
    logging.basicConfig(filename='milton.log',level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(filename)s:%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(filename)s:%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class AdminCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Logs errors
        """
        logging.info(repr(error))

    @commands.command()
    async def banlist(self, ctx):
        """
        Returns ban list
        """
        banned = checks.creds.banned
        if len(banned) == 0:
            await ctx.send("No users banned. Congratulations on your good behavior!")
        else:
            formatted_message = "Banned users\n----------\n"
            for user in banned:
                try:
                    member = ctx.guild.get_member(user)
                    formatted_message += member.nick if member.nick is not None else member.name
                    formatted_message += "\n"
                except commands.ConversionError as e:
                    logger.info("Error converting user " + str(user))
                    logger.info(e)
            await ctx.send(formatted_message)

    @commands.command()
    async def modlist(self, ctx):
        """
        Returns mod list
        """
        mods = checks.creds.mods
        if len(mods) == 0:
            await ctx.send("No mods at this time.")
        else:
            formatted_message = "Mods\n----------\n"
            for user in mods:
                try:
                    member = ctx.guild.get_member(user)
                    formatted_message += member.nick if member.nick is not None else member.name
                    formatted_message += "\n"
                except commands.ConversionError as e:
                    logger.info("Error converting user " + str(user))
                    logger.info(e)
            await ctx.send(formatted_message)

    @commands.command()
    async def godlist(self, ctx):
        """
        Returns admin list
        """
        gods = checks.creds.gods
        if len(gods) == 0:
            await ctx.send("God is dead.")
        else:
            formatted_message = "Admin users\n----------\n"
            for user in gods:
                try:
                    member = ctx.guild.get_member(user)
                    formatted_message += member.nick if member.nick is not None else member.name
                    formatted_message += "\n"
                except commands.ConversionError as e:
                    logger.info("Error converting user " + str(user))
                    logger.info(e)
            await ctx.send(formatted_message)

    @checks.is_mod()
    @commands.command()
    async def ban(self, ctx, user: discord.Member):
        if user.id not in checks.creds.gods and user.id not in checks.creds.mods:
            await checks.creds.add_banned(user.id)
            await ctx.send(str(user) + " has been banished from my garden.")

    @checks.is_mod()
    @commands.command()
    async def unban(self, ctx, user: discord.Member):
        if user.id in checks.creds.banned:
            await checks.creds.rem_banned(user.id)
            await ctx.send("Welcome back into my garden, " + str(user))
    
    @checks.is_owner()
    @commands.command()
    async def makemod(self, ctx, user: discord.Member):
        if user.id not in checks.creds.gods:
            await checks.creds.add_mod(user.id)
            await ctx.send(str(user) + " has been annointed as one of my messengers.")

    @checks.is_owner()
    @commands.command()
    async def unmod(self, ctx, user: discord.Member):
        if user.id in checks.creds.mods:
            await checks.creds.rem_mod(user.id)
            await ctx.send(str(user) + " is no longer a messenger of mine.")


    
            