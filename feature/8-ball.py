# Add this text to your main bot file
#이 텍스트를 메인 봇 파일에 추가 [이거 번역 된 한국어 몰라요]



import discord
from discord.ext import commands
import random



choices = ["It is certain",
"Without a doubt",
"You may rely on it",
"Yes definitely",
"It is decidedly so",
"As I see it, yes",
"Most likely",
"Yes",
"Outlook good",
"Signs point to yes",
"Reply hazy try again,
"Better not tell you now",
"Ask again later",
"Cannot predict now",
"Concentrate and ask again",
"Don’t count on it",
"Outlook not so good",
"My sources say no",
"Very doubtful",
"My reply is no",]


client = commands.Bot(command_prefix = '!')

@client.event
async def eightball(ctx):
    await ctx.send(random.choice(choices))


# Dont forgot to add token here
# 여기에 토큰을 추가하는 것을 잊지 마십시오 [i dont know koren this is translated]
client.run("Your Token")