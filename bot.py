import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import time
import random
import traceback
import asyncio
import re
import urllib
from bs4 import BeautifulSoup
import unicodedata
import json

token = '<your Token>'
#Naver Open API application ID
client_id = "<your_API_id>"
#Naver Open API application token
client_secret = "<your_API_Token>"

client = discord.Client() # Create Instance of Client. This Client is discord server's connection to Discord Room
bot = commands.Bot(command_prefix = '>>')

# bot이 준비되면 출력됩니다.
@client.event
async def on_ready():
    print('{0.user}을 로그인 완료했습니다.'.format(client))
# bot.py 부분 

@bot.command(name='99', help = '99의 인용구를 랜덤으로 출력합니다.')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='랜덤샘플링', help='최대치,갯수를 입력하면 랜덤으로 샘플링하여 숫자를 출력합니다.')
async def random_sampling(ctx, number_of_dice: int, number_of_sides: int):
    if (number_of_dice > 10) :
        dice = ["10번 이하로 입력해주세요."]
    
    else :
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
    await ctx.send(', '.join(dice))

@bot.command(name='채널생성')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'새로운 채널을 만들었습니다 : {channel_name}')
        await guild.create_text_channel(channel_name)


# dice.py

@bot.command(name='주사위')
async def roll(ctx, number: int):
    await ctx.send(f'주사위를 굴려 {random.randint(1,number)}이(가) 나왔습니다. (1-{number})')

@roll.error
async def roll_error(ctx, error):
    await ctx.send(f"2 이상의 정수를 넣어주세요!\nex) /주사위 6")

# status.py

@bot.command(name='방해금지')
@commands.is_owner()
async def dnd(ctx):
    await client.change_presence(status=discord.Status.dnd)
    await ctx.send('봇 상태를 방해금지로 변경했습니다.')

@bot.command(name='온라인')
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

# translate.py

@client.event
async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return

# on message의 COVID19-info
    if message.content.startswith(">>코로나"):
        # 보건복지부 코로나 바이러스 정보사이트"
        covidSite = "http://ncov.mohw.go.kr/index.jsp"
        covidNotice = "http://ncov.mohw.go.kr"
        html = urlopen(covidSite)
        bs = BeautifulSoup(html, 'html.parser')
        latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
        statisticalNumbers = bs.findAll('span', {'class': 'num'})
        beforedayNumbers = bs.findAll('span', {'class': 'before'})

        #주요 브리핑 및 뉴스링크
        briefTasks = []
        mainbrief = bs.findAll('a',{'href' : re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
        for brf in mainbrief:
            container = []
            container.append(brf.text)
            container.append(covidNotice + brf['href'])
            briefTasks.append(container)
        print(briefTasks)

        # 통계수치
        statNum = []
        # 전일대비 수치
        beforeNum = []
        for num in range(7):
            statNum.append(statisticalNumbers[num].text)
        for num in range(4):
            beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

        totalPeopletoInt = statNum[0].split(')')[-1].split(',')
        tpInt = ''.join(totalPeopletoInt)
        lethatRate = round((int(statNum[3]) / int(tpInt)) * 100, 2)
        embed = discord.Embed(title="Covid-19 Virus Korea Status", description="",color=0x5CD1E5)
        embed.add_field(name="Data source : Ministry of Health and Welfare of Korea", value="http://ncov.mohw.go.kr/index.jsp", inline=False)
        embed.add_field(name="Latest data refred time",value="해당 자료는 " + latestupdateTime[0] + "월 " + latestupdateTime[1] + "일 "+latestupdateTime[2] +" 자료입니다.", inline=False)
        embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1]+"("+beforeNum[0]+")",inline=True)
        embed.add_field(name="완치환자", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
        embed.add_field(name="치료중", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
        embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
        embed.add_field(name="누적확진률", value=statNum[6], inline=True)
        embed.add_field(name="치사율", value=str(lethatRate) + " %",inline=True)
        embed.set_thumbnail(url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")
        await message.channel.send("Covid-19 Virus Korea Status", embed=embed)



    '''
    #You can get id and secret key with registering in naver
    client_id = ""
    client_secret = ""
    #Text to translate
    entData = quote("")
    dataParmas = "source=en&target=id&text=" + entData
    baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    #Make a Request Instance
    request = Request(baseurl)
    #add header to packet
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urlopen(request,data=dataParmas.encode("utf-8"))
    responsedCode = response.getcode()
    if(responsedCode==200):
        response_body = response.read()
        #response_body -> byte string : decode to utf-8
        api_callResult = response_body.decode('utf-8')
        #JSON Type data will be printed. So need to make it back to type JSON(like dictionary)
        stringConvertJSON = api_callResult.replace("'","\"")
        api_callResult = json.loads(stringConvertJSON)
        translatedText = api_callResult['message']['result']["translatedText"]
        print(translatedText)
    else:
        print("Error Code : " + responsedCode)
    '''
    
    if message.content.startswith(">>한영번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        #띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                print(combineword)
                # Make Query String.
                dataParmas = "source=ko&target=en&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> English", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated English", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="API provided by Naver Open API")
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")


    if message.content.startswith(">>영한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=en&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | English -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="English to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="API provided by Naver Open API")
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith(">>한일번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ko&target=ja&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> Japanese", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Japanese", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="API provided by Naver Open API")
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith(">>일한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                dataParmas = "source=ja&target=ko&text=" + combineword
                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')

                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Japanese -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="Japanese to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="API provided by Naver Open API")
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith(">>한중번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.

                #Simplified Chinese
                dataParmas = "source=ko&target=zh-CN&text=" + combineword

                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> Chinese(Simplified Chinese)", description="", color=0x5CD1E5)
                    embed.add_field(name="Korean to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Chinese(Simplified)", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="API provided by Naver Open API")
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith(">>중한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                # if entered value is sentence, assemble again and strip blank at both side
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                # Make Query String.
                # Simplified Chinese
                dataParmas = "source=zh-CN&target=ko&text=" + combineword


                # Make a Request Instance
                request = Request(baseurl)
                # add header to packet
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()
                    # response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                    api_callResult = json.loads(api_callResult)
                    # Final Result
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Chinese -> Korean", description="", color=0x5CD1E5)
                    embed.add_field(name="Chinese to translate", value=savedCombineword, inline=False)
                    embed.add_field(name="Translated Korean", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                    embed.set_footer(text="API provided by Naver Open API")
                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

# Covid19-Info source code 
#The code above was created by modifying the code from
#https://github.com/J-hoplin1/Covid19-Information-bot

# translate.py source code
#The code above was created by modifying the code from
#https://github.com/J-hoplin1/Papago-API-Translate-Bot

client.run(token)