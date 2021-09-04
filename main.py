import pypxl
import time
import requests

webhook_onoff = "https://discord.com/api/webhooks/883775606540632075/hHrdNa-UHAaerqtoBWMdnenBsi0Tfd1-zsW78hPEIenvHNN1EA8IvEiNGvanko7zqiL_"
webhook_mvp = "https://discord.com/api/webhooks/835654940008382464/RsN3Jjg8B6Ukv-8C09MfjktvyGrQztO4At2RIf27w4ZwmLpq_olf7kjr_YXPyAE8Cv43"
webhook_global = "https://discord.com/api/webhooks/835654823784874015/yXIkpU5K7mjAcJc3bBorIkaApkH5cw5Sc-_rdoKrJo-Jfxfmuyabk7C1MYtU8Nmtegit"
webhook_stats = "https://discord.com/api/webhooks/883773760447066112/qzeDM4A882s1DmvM7OXyswue_fQCnZL-F2xDu-iIyk5mB7CAN7ZmjJj1Gspz-ThQ5ezS"

#/8 Bot
bot8 = pypxl.Bot("pbt_ttt_6", '85*0zCHaNlAPbVm%bB^EC', 8)
#/7 Bot
bot7 = pypxl.Bot("pbt_ttt_5", "Ls7Wi041AA97YvST13m0xq", 7)

@bot7.socketconnection.on("chat.user.message")
def logChat7(data):
    messageUsername = data["username"]
    messageGuild = data["guild"]
    message = data["message"]
    messageIcons = data["icons"]
    messageChannel = data["channel"]
    messageMention = data["mention"]
    if messageChannel == "global":
        content = """
		{message}
		Mentioned People:{messageMention}
		"""
        emojis = getBadges(messageIcons)
        content2 = """
        Badges> {emojis}
        Logged <t:{timestamp}:R>
        """
        timestamp = getTimeStamp()
        embed = {"description": f"{content}","title": "/7 Chat Message"}
        whdata = {"content": f"{content2}","username": "{messageUsername} - {messageGuild}","embeds": [embed],}
        postWebhook(webhook_global, whdata)
		#Automod
		#checkChatMessage()

@bot8.socketconnection.on("chat.user.message")
def logChat8(data):
	messageUsername = data["username"]
	messageGuild = data["guild"]
	message = str(data["message"])
	messageIcons = data["icons"]
	messageChannel = data["channel"]
	messageMention = data["mention"]
	if messageChannel == "painting":
		content = """
		{message}
		Mentioned People:{messageMention}
		"""
        emojis = getBadges(messageIcons)
        content2 = """
        Badges> {emojis}
        Logged <t:{timestamp}:R>
        """
        timestamp = getTimeStamp()
        embed = {"description": f"{content}","title": "/8 Chat Message"}
        whdata = {"content": f"{content2}:R>","username": "{messageUsername} - {messageGuild}","embeds": [embed],}
    	postWebhook(webhook_mvp, whdata)
		#Automod
		#checkChatMessage()

#get /8 Specific Data
@bot8.socketconnection.on("chat.stats")
def update8Stats(data):
	global canvas8Stat 
	canvas8Stat = data[0]

@bot7.socketconnection.on("chat.stats")
def postChatStats(data):
    canvas7Stat = data[0]
    totalStat = data[1]
    content = f"""
    Players on Canvas 7>{canvas7Stat}
    Players on Canvas 7>{canvas8Stat}
    Players in total>{totalStat}"""
    timestamp = getTimeStamp()
    embed = {"description": f"{content}","title": "Stats"}
    whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Stats","embeds": [embed],}
    postWebhook(webhook_stats, whdata)

@bot7.socketconnection.on("j")
def postJoins(data):
	content = f"{data} joined!"
	timestamp = getTimeStamp()
	embed = {"description": f"{content}","title": "Joins"}
	whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Joins","embeds": [embed],}
	postWebhook(webhook_onoff, whdata)

@bot7.socketconnection.on("l")
def postLeaves(data):
    content = f"{data} left!"
    timestamp = getTimeStamp()
    embed = {"description": f"{content}","title": "Leaves"}
    whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Leaves","embeds": [embed],}
    postWebhook(webhook_onoff, whdata)
	#gonna gi get food ~15 min
def checkChatMessage(message,username,canvas):
    spltmsg = message.split()
    with open('filter.txt') as filter:
        for slur in filter.read():
            for word in spltmsg:
                if slur.contains(f"{word}"):
                    bot7.send_Chat("You have sent a message in chat which is against PixelPlace Terms of Service. The Staff Team will be informed",f"{username}","whispers",f"{username}")
                    time.sleep(0.8)
                    bot7.send_Chat("Please refrain from doing so in the future or your account will be muted.",f"{username}","whispers",f"{username}")
                    timestamp = getTimeStamp()
                    content = """
                    {username} said {message}.
                    <@&835970992819273748>
                    """
                    embed = {"description": f"{content}","title": "Bad word detected!"} 
                    whdata = {"content": f"Logged <t:{timestamp}:R>","username": "Mods alerts","embeds": [embed],}
                    postWebhook(webhook_stats, whdata)

def getBadges(messageIcons):
    emojilist = []
    #idk if this will work first try
    #"icons":["1-year","moderator","nitro","bread"]
    for iconname in messageIcons:
        emojilist.append(f":{iconname}:")
    return emojilist

def getTimeStamp():
	epoch = str(time.time()).split(".")[0]
	return epoch

def postWebhook(url, data):
    result = requests.post(url, json=data)
    if 200 <= result.status_code < 300:
        print(f"Webhook sent {result.status_code}")
    else:
        print(f"Not sent with {result.status_code}, response:\n{result.json()}")