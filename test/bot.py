import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import random

if __name__ == '__main__':
  py_ver = int(f"{sys.version_info.major}{sys.version_info.minor}")
  if py_ver > 37 and sys.platform.startswith('win'):
  	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix = '>>')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)