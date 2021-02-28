import discord
import logging
import random
import asyncio
import re , os
import time
from discord.ext import commands
import traceback

logger_debug = logging.getLogger('discord')
logger_debug.setLevel(logging.DEBUG)
handler_d = logging.FileHandler(filename='discord_debug.log', encoding='utf-8', mode='w')
handler_d.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger_debug.addHandler(handler_d)

logger_info =logging.getLogger('discord')
logger_info.setLevel(logging.INFO)
handler_i = logging.FileHandler(filename='discord_info.log', encoding='utf-8', mode='w')
handler_d.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger_info.addHandler(handler_i)

TOKEN=os.environ["ONWBot"]

INITIAL_EXTENSIONS = [
    'cogs.OneNight'
]

class OneNightBot(commands.Bot):

    def __init__(self,command_prefix="/",owner_id=None,intents=None):
        super().__init__(command_prefix=command_prefix,owner_id=owner_id,intents=intents)
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print("Logged in as",end=" ")
        print(client.user.name)
        print("===============")
        await client.change_presence(activity=discord.Activity(name="test bot"))

if __name__=="__main__":
    intents=discord.Intents.all()
    client = OneNightBot(intents=intents)
    client.run(TOKEN)