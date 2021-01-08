from discord.ext import commands
import utils
import logging, os

if (os.environ.get("LOGGING_MODE") == 'file'):
    logging.basicConfig(filename='milton.log',level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(filename)s:%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
else:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(filename)s:%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class CheckCreds:
    def __init__(self):
        self.gods = []
        self.mods = []
        self.banned = []

    async def sync_mods(self):
        try:
            response = await utils.user_get({"role": "M"})
            self.mods = []
            for user in response:
                self.mods.append(user['user_id'])
            logger.info("Mods synced")
        except:
            pass

    async def sync_banned(self):
        try:
            response = await utils.user_get({"role": "B"})
            self.banned = []
            for user in response:
                self.banned.append(user['user_id'])
            logger.info("Bans synced")
        except:
            pass

    async def sync_gods(self):
        try:
            response = await utils.user_get({"role": "A"})
            self.gods = []
            for user in response:
                self.gods.append(user['user_id'])
            logger.info("Gods synced")
        except:
            pass

    async def add_mod(self,uid):
        try:
            response = await utils.user_patch({
                                                "user_id": uid,
                                                "role": "M"}, uid)
            await self.sync_mods()
        except:
            pass

    async def rem_mod(self, uid):
        try:
            response = await utils.user_patch({
                                                "user_id": uid,
                                                "role": "N"}, uid) # User goes back to normal
            await self.sync_mods()
        except:
            pass

    async def add_banned(self, uid):
        if uid not in self.gods:
            try:
                response = await utils.user_patch({
                                                    "user_id": uid,
                                                    "role": "B"}, uid)
                await self.sync_banned()
            except:
                pass

    async def rem_banned(self, uid):
        try:
            response = await utils.user_patch({
                                                "user_id": uid,
                                                "role": "N"}, uid) # User goes back to normal
            await self.sync_banned()
        except:
            pass

class spamState: # Rate limiting class
    def __init__(self):
        self.spam_dict = {}

    def incrSpam(self, authId):
        if authId not in self.spam_dict:
            self.spam_dict[authId] = 1
        elif self.spam_dict[authId] < 5:
            self.spam_dict[authId] += 1
        else:
            self.spam_dict[authId] = 5

    def flush(self):
        self.spam_dict = {}

creds = CheckCreds()
spam = spamState()

def is_owner_check(ctx):
    return ctx.author.id in creds.gods

def is_owner(): # see master_check comments
    return commands.check(is_owner_check)

def is_mod_check(ctx):
    return is_owner_check(ctx) or ctx.author.id in creds.mods

def is_mod(): # see master_check comments
    return commands.check(is_mod_check)

def _master_check(ctx): #see discord bot.py and commands files, plus Red-Bot for remembering how you figured this out
    if is_owner_check(ctx): #It had to do with a lot of decorators and callables
        return True
    elif ctx.author.id in creds.banned:
        return False
    elif ctx.author.bot:
        return False
    elif ctx.author.id in spam.spam_dict:
        if spam.spam_dict[ctx.author.id] == 5:
            return False
        else:
            return True
    else:
        return True

def master_check(bot): # add master check to bot
    bot.check(_master_check)