import discord
import traceback
import asyncio
import re
from discord.ext import commands

client = commands.Bot(command_prefix='>>')

Token = ''

@client.event
async def on_ready():
    print('Bot is ready.')
    
@client.command(name='방해금지')
@commands.is_owner()
async def dnd(ctx):
    await client.change_presence(status=discord.Status.dnd)
    await ctx.send('봇 상태를 방해금지로 변경했습니다.')

@client.command(name='온라인')
@commands.is_owner()
async def online(ctx):
    await client.change_presence(status=discord.Status.online)
    await ctx.send('봇 상태를 온라인으로 변경했습니다.')

@client.event
async def on_command_error(ctx, error):
    tb = traceback.format_exception(type(error), error, error.__traceback__)
    err = [line.rstrip() for line in tb]
    errstr = '\n'.join(err)
    if isinstance(error, commands.NotOwner):
        await ctx.send('봇 주인만 사용 가능한 명령어입니다')
    else:
        print(errstr)

client.run(Token)
