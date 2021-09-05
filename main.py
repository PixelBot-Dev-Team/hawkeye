import pypxl
import time
import requests
import threading
import datetime
import matplotlib.pyplot as plt
import numpy as np


webhook_onoff = "https://discord.com/api/webhooks/883775606540632075/hHrdNa-UHAaerqtoBWMdnenBsi0Tfd1-zsW78hPEIenvHNN1EA8IvEiNGvanko7zqiL_"
webhook_mvp = "https://discord.com/api/webhooks/835654940008382464/RsN3Jjg8B6Ukv-8C09MfjktvyGrQztO4At2RIf27w4ZwmLpq_olf7kjr_YXPyAE8Cv43"
webhook_global = "https://discord.com/api/webhooks/835654823784874015/yXIkpU5K7mjAcJc3bBorIkaApkH5cw5Sc-_rdoKrJo-Jfxfmuyabk7C1MYtU8Nmtegit"
webhook_stats = "https://discord.com/api/webhooks/883773760447066112/qzeDM4A882s1DmvM7OXyswue_fQCnZL-F2xDu-iIyk5mB7CAN7ZmjJj1Gspz-ThQ5ezS"
webhook_mods = "https://discord.com/api/webhooks/883807042656157828/053ufcOenaZo0dZHqBhz1Fd47SAt4qQ5_Wd3ZIMPo_RRcIGbBqguw1zjULrsS2QCMyJ0"

start_time = datetime.datetime.utcnow()

def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return bg_f

#/8 Bot
bot8 = pypxl.Bot("pbt_ttt_6", '85*0zCHaNlAPbVm%bB^EC', 8)
#/7 Bot
bot7 = pypxl.Bot("pbt_ttt_5", "Ls7Wi041AA97YvST13m0xq", 7)

onlineUsersHistory = [21, 43, 19, 83, 21] #test

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
    if messageChannel == "global":
        if messageMention == "":
            messageMention = "None"
        content = f"""
        {message}
        Mentioned People:{messageMention}
        """
        timestamp = getTimeStamp()
        content2 = f"Logged <t:{timestamp}:R>"
        timestamp = getTimeStamp()
        embed = {"description": f"{content}","title": "/7 Chat Message"}
        whdata = {"content": f"{content2}","username": f"{messageUsername} - {messageGuild}","embeds": [embed],}
        postWebhook(webhook_global, whdata)
        checkChatMessage(message, messageUsername)

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
        content = f"""
        {message}
        Mentioned People:{messageMention}
        """
        timestamp = getTimeStamp()
        content2 = f"Logged <t:{timestamp}:R>"
        embed = {"description": f"{content}","title": "/8 Chat Message"}
        whdata = {"content": f"{content2}","username": f"{messageUsername} - {messageGuild}","embeds": [embed],}
        postWebhook(webhook_mvp, whdata)
        checkChatMessage(message, messageUsername)

@bot7.socketconnection.on("chat.stats")
@background
def postChatStats(data):
    canvas7Stat = data[0]
    totalStat = data[1]
    content = f"""
    Players on Canvas 7>{canvas7Stat}
    Players in total>{totalStat}"""
    timestamp = getTimeStamp()
    embed = {"description": f"{content}","title": "Stats", "color": 16776958} #white
    whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Stats","embeds": [embed],}
    postWebhook(webhook_stats, whdata)

@bot7.socketconnection.on("j")
@background
def postJoins(data):
    if data != "":
        content = f"{data} joined!"
        timestamp = getTimeStamp()
        embed = {"description": f"{content}","title": "Joins", "color": 2531122} #green
        whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Joins","embeds": [embed],}
        postWebhook(webhook_onoff, whdata)
        file = open(f"{CurrentDir}\\banned.txt",'r')
        banned = file.read().splitlines()
        username.lower
        for name in banned:
            name.lower()
            if banned in username:
                timestamp = getTimeStamp()
                embed = {"description": f"Logged <t:{timestamp}:R>","title": "Permabanned User Detected!", "fields" : [{"name" : "Username", "value" : f"{username}"}], "color": 13571349} #red
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

#check at a later point https://forms.gle/Ti9BoJEmDvzVGnwq7
def checkChatMessage(message,username):
    spltmessage = message.split()
    file = open(f"{CurrentDir}\\filter.txt",'r')
    slurlist = file.read().splitlines()
    for word in spltmessage:
        word.lower()
        if word in slurlist:
            bot7.send_Chat("You have sent a message in chat which is against PixelPlace Terms of Service. The Staff Team will be informed.",f"{username}","whispers",f"{username}", 21)
            time.sleep(0.8)
            bot7.send_Chat("Please refrain from doing so in the future or your account will be muted.",f"{username}","whispers",f"{username}", 21)
            timestamp = getTimeStamp()
            embed = {"description": f"Logged <t:{timestamp}:R>","title": "Bad word detected!", "fields" : [{"name" : "Username", "value" : f"{username}"}, {"name" : "Message", "value" : f"{message}"}], "color": 14662147} #yellow
            whdata = {"content": "<@&835970992819273748>","username": "AutoMod","embeds": [embed],}
            postWebhook(webhook_mods, whdata)            
        file.close()
    
def getTimeStamp():
	epoch = str(time.time()).split(".")[0]
	return epoch

def createChart(history):
    plt.plot(history)
    plt.show()

def postWebhook(url, data):
    result = requests.post(url, json=data)
    if 200 <= result.status_code < 300:
        print(f"Webhook sent {result.status_code} - Data: {data}")
    else:
        print(f"Not sent with {result.status_code}, response:\n{result.json()}")

if __name__ == "__main__":
    createChart()
    while True:
        time.sleep(99999)

#TODO
#Add check if data is same for leave/join
#use sql lite thing
#pray icons work
#MaKe EmBeDs PrEtTy
#user icons