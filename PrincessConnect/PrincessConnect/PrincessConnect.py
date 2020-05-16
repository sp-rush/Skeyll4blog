from discord.ext import tasks
from datetime import datetime, timedelta, timezone
import discord
import os

TOKEN = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()
CHANNEL_ID = 607555169751793674
JST = timezone(timedelta(hours=+9), 'JST')

RoundCount = 0 # 周回数
StageCount = 0 # 段階数
DateCount = 0 # 日数
DateCountLast = 0 # 最終日
BossNum = ["1","2","3","4","5"] # ボス番号
BossList = ["0","ミノタウロス","トライロッカー","メガラパーン","ワイルドグリフォン","ゴブリングレート"] # ボス名前
BossHP = 0 # ボスHP
LoginList = [] #参戦メンバーリスト
Booking1 = ["すぷ","コペ丸"] # 予約を追加するリスト
Booking2 = [] # book→予約
Booking3 = []
Booking4 = []
Booking5 = []

@tasks.loop(seconds=10)
async def auto():
    now = datetime.now(JST).strftime("%H:%M")
    if now == "05:00":
        channel = client.get_channel(CHANNEL_ID)
        await channel.send("ランドソルの日付が変わりました！")

@client.event
async def on_message(message):
    listFlag = 0
    bookFlag = 0
    endFlag = 0
    displayFlag = 0
    
    if message.content.startswith("rsv"):
        if "list" in message.content: # Call a list
            listFlag = 1
        elif "END" in message.content: # Initialize all lists
            endFlag = 1
        elif "!" in message.content: # Call all arrays
            displayFlag = 1
        else: # Book
            bookFlag = 1

        if listFlag == 1:
            for Boss in BossNum:
                tmpList = []
                if Boss in message.content:
                    BookList = "Booking" + Boss
                    tmpList = [x[0] for x in eval(BookList)]
                    member = ""
                    for one in tmpList:
                        member += one + " "
                    await message.channel.send("Boss" + Boss + ":" + member)
            listFlag =  0

        elif endFlag == 1:
            for Boss in BossNum:
                    BookList = "Booking" + Boss
                    eval(BookList).clear()
            reply = "予約を全削除"
            await message.channel.send(reply)
            endFlag = 0

        elif bookFlag == 1:
            reply = message.author.display_name + "さんを"
            for i in BossNum:
                if i in message.content:
                    BookList = "Booking" + i
                    eval(BookList).append([message.author.display_name, str(message.author.mention)])
                BossName = BossList[int(i)]
                reply += BossName + " "
            reply += BossName + " に予約しました。"
            if reply == message.author.display_name + "さんを に予約しました。":
                reply = "予約できませんでした。"
            await message.channel.send(reply)
            bookFlag = 0

        elif displayFlag == 1: # Display all book list
            for Boss in BossNum:
                tmpList = []
                BookList = "Booking" + Boss
                tmpList= [x[0] for x in eval(BookList)]
                member = ""
                for one in tmpList:
                    member += one + " "
                await message.channel.send("Boss" + Boss + ":" + member)
            displayFlag = 0

    elif message.content.startswith("fin"):
        for Boss in BossNum:
                if Boss in message.content:
                    BookList = "Booking" + Boss
                    eval(BookList).remove([message.author.display_name,str(message.author.mention)]) 
        reply = "削除完了 >" + message.author.display_name
        await message.channel.send(reply)

    elif message.content.startswith("ment"):
        for Boss in BossNum:
            tmpList = []
            if Boss in message.content:
                BookList = "Booking" + Boss
                tmpList = [x[1] for x in eval(BookList)]
                member = ""
                for one in tmpList:
                    member += one + " "
                await message.channel.send("Boss" + Boss + ":" + member)
    
    elif message.content.startswith("cmd"):
        reply = "予約:rsv 1-5 / 予約表示:rsv list 1-5 / 予約全表示:rsv! / 予約削除:fin 1-5 / 予約全削除:rsv END / 通知:ment 1-5"
        await message.channel.send(reply)

auto.start()
client.run(TOKEN)
