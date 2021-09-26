import datetime
import pathlib
import sqlite3
import threading
import time
from io import DEFAULT_BUFFER_SIZE

import matplotlib.pyplot as plt
import requests

import pypxl

webhook_onoff = "https://discord.com/api/webhooks/883775606540632075/hHrdNa-UHAaerqtoBWMdnenBsi0Tfd1-zsW78hPEIenvHNN1EA8IvEiNGvanko7zqiL_"
webhook_mvp = "https://discord.com/api/webhooks/835654940008382464/RsN3Jjg8B6Ukv-8C09MfjktvyGrQztO4At2RIf27w4ZwmLpq_olf7kjr_YXPyAE8Cv43"
webhook_global = "https://discord.com/api/webhooks/835654823784874015/yXIkpU5K7mjAcJc3bBorIkaApkH5cw5Sc-_rdoKrJo-Jfxfmuyabk7C1MYtU8Nmtegit"
webhook_stats = "https://discord.com/api/webhooks/883773760447066112/qzeDM4A882s1DmvM7OXyswue_fQCnZL-F2xDu-iIyk5mB7CAN7ZmjJj1Gspz-ThQ5ezS"
webhook_mods = "https://discord.com/api/webhooks/883807042656157828/053ufcOenaZo0dZHqBhz1Fd47SAt4qQ5_Wd3ZIMPo_RRcIGbBqguw1zjULrsS2QCMyJ0"
webhook_mutes = "https://discord.com/api/webhooks/888503958904119356/t-v4e44YADLH7x5mF68XSj0nYKcV07dDRGFQ7z6fmkPTQnqBZ6bIAlfoECU_1Z7sjkOc"

iconlist = {"_1_month" : "<:1month:883780503583465532>","_1_year" : "<:1year:883780503369568277>","_3_months" : "<:3months:883780503440871465>","_admin" : "<:admin:883780503323430933>","_booster" : "<:booster:883780503596060712>","_ppbread" : "<:ppbread:883780503713488916>","_chatmoderator" : "<:chatmoderator:883780503386357781>","_gifter" : "<:gifter:883780503646392370>","_moderator" : "<:moderator:883780503566704710>","_nitro" : "<:nitro:883780503675764736>","_paintingmoderator" : "<:paintingmoderator:883780503151460373>","_paintingowner" : "<:paintingowner:883780503780601866>","_partner" : "<:partner:883780503558299658>","_vip" : "<:vip:883780503516377108>"}

global start_time
start_time = datetime.datetime.utcnow()

CurrentDir = pathlib.Path(__file__).parent.absolute()

def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return bg_f

#/8 Bot
bot8 = pypxl.Bot("ppbt_logbot", ">,PDF[e<$aDQ[2%=", 8)
bot8Players = {}
#/7 Bot
bot7 = pypxl.Bot("ppbt_logbot1", "8gD;Ky$EV+De6za5^", 7)
bot7Players = {}

timeHistory = []
onlineUsersHistory = [] #test

def chat_Safety_Check(data):
    createdAt = data["createdAt"]
    messagetime = datetime.datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%SZ")
    if messagetime > start_time and data["username"] != "TTTBot5" and data["username"] != "TTTBot6" and data["channel"] in ["global","painting"]:
        return True
    else:
        return False

@bot7.socketconnection.on("chat.user.message")
@background
def logChat7(data):
    print(data)
    if chat_Safety_Check(data) == True: 
        pass 
    else: 
        return
    messageUsername = data["username"]
    messageGuild = data["guild"]
    message = data["message"]
    if message == "":
        message = "/here"
    messageIcons = data["icons"]

    messageChannel = data["channel"]
    messageMention = data["mention"]
    if message == "!restart":
        print("restart")
        if messageUsername == "AlmosYT" or messageUsername == "SoManyNames":
            print("restart")
            global start_time
            start_time = datetime.datetime.utcnow()
            bot7.DisconnectFromSocket()
            bot8.DisconnectFromSocket()
    if messageChannel == "global":
        content = ""
        if messageMention == "":
            messageMention = "None"
            content = f"""
            {message}
            """
        else:
            content = f"""
            {message}
Mentioned People:{messageMention}
            """
        timestamp = getTimeStamp()
        iconstring = getIcons(messageIcons)
        content2 = f"Logged <t:{timestamp}:R>"
        timestamp = getTimeStamp()
        embed = {"description": f"{content}","title": f"{messageUsername} {iconstring} - {messageGuild}"}
        whdata = {"content": f"{content2}","username": f"/7 Chat Message","embeds": [embed],}
        postWebhook(webhook_global, whdata)
        checkChatMessage(message, messageUsername,7)

@bot8.socketconnection.on("chat.user.message")
@background
def logChat8(data):
    if chat_Safety_Check(data) == True:
        pass
    else:
        return
    messageUsername = data["username"]
    messageGuild = data["guild"]
    message = str(data["message"])
    if message == "":
        message = "/here"
    messageIcons = data["icons"]
    
    messageChannel = data["channel"]
    messageMention = data["mention"]
    if messageChannel == "painting":
        content = ""
        if messageMention == "":
            messageMention = "None"
            content = f"""
            {message}
            """
        else:
            content = f"""
            {message}
Mentioned People:{messageMention}
            """
        timestamp = getTimeStamp()
        iconstring = getIcons(messageIcons)
        content2 = f"Logged <t:{timestamp}:R>"
        embed = {"description": f"{content}","title": f"{iconstring}{messageUsername} - {messageGuild}"}
        whdata = {"content": f"{content2}","username": f"/8 Chat Message","embeds": [embed],}
        postWebhook(webhook_mvp, whdata)
        checkChatMessage(message, messageUsername,8)

@bot7.socketconnection.on("chat.stats")
@background
def postChatStats(data):
    canvas7Stat = data[0]
    totalStat = data[1]
    content = f"""
    Players on Canvas 7>{canvas7Stat}
Players in total   >{totalStat}"""
    timestamp = getTimeStamp()
    embed = {"description": f"{content}","title": "Stats", "color": 16776958} #white
    whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Stats","embeds": [embed],}
    postWebhook(webhook_stats, whdata)
    #postPlayersRequests()
    SaveOnlineData(canvas7Stat)
    

@background
def postPlayersRequests():
    bot7.socketconnection.emit(event="painting.players", data=7)
    bot8.socketconnection.emit(event="painting.players", data=8)
    time.sleep(4)

@bot7.socketconnection.on("painting.players")
@background
def handlePaintingPlayers7(data):
    bot7Players = data

@bot8.socketconnection.on("painting.players")
@background
def handlePaintingPlayers8(data):
    bot8Players = data

#chat.stats - Charts 

@background
def createChart():
    plt.title("PixelPlace Online Users (24h)")
    plt.suptitle("HawkEye")
    
    plt.plot(timeHistory, onlineUsersHistory)
    plt.gcf().autofmt_xdate()

    plt.savefig("chart.png") 

@background
def SaveOnlineData(onlineCountTotal):
    timeHistory.append(datetime.datetime.now())
    onlineUsersHistory.append(onlineCountTotal)


@bot7.socketconnection.on("j")
@background
def postJoins(data):
    if data != "":
        content = f"{data} joined!"
        timestamp = getTimeStamp()
        embed = {"description": f"{content}","title": "Joins", "color": 2531122} #green
        whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Joins","embeds": [embed],}
        postWebhook(webhook_onoff, whdata)
        file = open(f"{CurrentDir}/banned.txt",'r')
        bannedlist = file.read().splitlines()
        for name in bannedlist:
            if str(name) in data.lower():
                timestamp = getTimeStamp()
                embed = {"description": f"Logged <t:{timestamp}:R>","title": "Permabanned User Detected!", "fields" : [{"name" : "Username", "value" : f"{data}"}], "color": 13571349} #red
                whdata = {"content": "<@&835970992819273748>","username": "AutoMod","embeds": [embed],}
                postWebhook(webhook_mods, whdata)

@bot7.socketconnection.on("l")
@background
def postLeaves(data):
    content = f"{data} left!"
    timestamp = getTimeStamp()
    embed = {"description": f"{content}","title": "Leaves", "color": 13571349} #red
    whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Leaves","embeds": [embed],}
    postWebhook(webhook_onoff, whdata)

@bot7.socketconnection.on("chat.system.delete")
@background
def postMutes(data):
    print(data)
    timestamp = getTimeStamp()
    embed = {"description": f"Logged <t:{timestamp}:R>","title": "Chat Mute detected!", "fields" : [{"name" : "Muted User", "value" : f"{data}"}, {"name" : "Info", "value" : "These logs are not official information. To appeal a mute, join the PixelPlace discord."}], "color": 13036340} #yellow
    whdata = {"content": "","username": "Chat Mutes","embeds": [embed],}
    postWebhook(webhook_mutes, whdata)      

#To collect slurs: https://forms.gle/Ti9BoJEmDvzVGnwq7
def checkChatMessage(message,username,canvas):
    spltmessage = message.split()
    file = open(f"{CurrentDir}/filter.txt",'r')
    slurlist = file.read().splitlines()
    for word in spltmessage:
        if word.lower() in slurlist:
            bot7.send_Chat("You have sent a message in chat which is against PixelPlace Terms of Service. The Staff Team will be informed.",f"{username}","whispers",f"{username}", 21)
            time.sleep(0.8)
            bot7.send_Chat("Please refrain from doing so in the future or your account will be muted.",f"{username}","whispers",f"{username}", 21)
            timestamp = getTimeStamp()
            embed = {"description": f"Logged <t:{timestamp}:R>","title": "Bad word detected!", "fields" : [{"name" : "Username", "value" : f"{username}"}, {"name" : "Canvas", "value" : f"{canvas}"}, {"name" : "Message", "value" : f"{message}"}, {"name" : "Detected Word", "value" : f"{word}"}], "color": 14662147} #yellow
            whdata = {"content": "<@&835970992819273748>","username": "AutoMod","embeds": [embed],}
            postWebhook(webhook_mods, whdata)            
        file.close()
    file1 = open(f"{CurrentDir}/softfilter.txt",'r')
    slurlist1 = file1.read().splitlines()
    for word in spltmessage:
        if word.lower() in slurlist1:
            bot7.send_Chat("You have sent a message in chat which might be against PixelPlace Terms of Service.",f"{username}","whispers",f"{username}", 21)
            time.sleep(0.8)
            bot7.send_Chat("Please refrain from doing so in the future or your account will be muted.",f"{username}","whispers",f"{username}", 21)
            timestamp = getTimeStamp()
            embed = {"description": f"Logged <t:{timestamp}:R>","title": "Soft Alert - Bad word detected!", "fields" : [{"name" : "Username", "value" : f"{username}"}, {"name" : "Message", "value" : f"{message}"}, {"name" : "Canvas", "value" : f"{canvas}"}, {"name" : "Detected Word", "value" : f"{word}"}], "color": 13036340} #yellow
            whdata = {"content": "","username": "AutoMod","embeds": [embed],}
            postWebhook(webhook_mods, whdata)            
        file.close()
    file = open(f"{CurrentDir}/banned.txt",'r')
    banned = file.read().splitlines()
    if username.lower() in str(banned):
        timestamp = getTimeStamp()
        embed = {"description": f"Logged <t:{timestamp}:R>","title": "Permabanned User Detected!", "fields" : [{"name" : "Username", "value" : f"{username}"}], "color": 13571349} #red
        whdata = {"content": "<@&835970992819273748>","username": "AutoMod","embeds": [embed],}
        postWebhook(webhook_mods, whdata)
    
def getTimeStamp():
	epoch = str(time.time()).split(".")[0]
	return epoch

def getIcons(icons):
	iconsstr = ""
	for icon in icons:
		icon = icon.replace("-", "_")
		icon = f"_{icon}"
		if icon == "_bread":
			icon = "_ppbread"
		formatted_icon = iconlist[f"{icon}"]
		iconsstr = f"{iconsstr}{formatted_icon}"
	return iconsstr
        
def postWebhook(url, data):
    result = requests.post(url, json=data)
    if 200 <= result.status_code < 300:
        print(f"Webhook sent {result.status_code} - Data: {data}")
    else:
        print(f"Not sent with {result.status_code}, response:\n{result.json()}")

if __name__ == "__main__":
    time.sleep(45)
    createChart()
    while True:
        time.sleep(1800)
        createChart()