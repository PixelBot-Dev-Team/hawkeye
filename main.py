# sourcery skip: aware-datetime-for-utc
import datetime
import pathlib
import threading
import time
import socketio
import requests

CurrentDir = pathlib.Path(__file__).parent.absolute()

webhook_onoff = "https://discord.com/api/webhooks/883775606540632075/hHrdNa-UHAaerqtoBWMdnenBsi0Tfd1-zsW78hPEIenvHNN1EA8IvEiNGvanko7zqiL_"
webhook_mvp = "https://discord.com/api/webhooks/835654940008382464/RsN3Jjg8B6Ukv-8C09MfjktvyGrQztO4At2RIf27w4ZwmLpq_olf7kjr_YXPyAE8Cv43"
webhook_global = "https://discord.com/api/webhooks/835654823784874015/yXIkpU5K7mjAcJc3bBorIkaApkH5cw5Sc-_rdoKrJo-Jfxfmuyabk7C1MYtU8Nmtegit"
webhook_stats = "https://discord.com/api/webhooks/883773760447066112/qzeDM4A882s1DmvM7OXyswue_fQCnZL-F2xDu-iIyk5mB7CAN7ZmjJj1Gspz-ThQ5ezS"
webhook_mods = "https://discord.com/api/webhooks/883807042656157828/053ufcOenaZo0dZHqBhz1Fd47SAt4qQ5_Wd3ZIMPo_RRcIGbBqguw1zjULrsS2QCMyJ0"
webhook_mutes = "https://discord.com/api/webhooks/888503958904119356/t-v4e44YADLH7x5mF68XSj0nYKcV07dDRGFQ7z6fmkPTQnqBZ6bIAlfoECU_1Z7sjkOc"
webhook_nonenglish = "https://discord.com/api/webhooks/1069645268808634463/nyWeuJnVh9wVealJiUg6mV0wqXVb0SsJoRmB5j2GXGu1wOCxABXbclQRXG8eFHR-LbCm"
webhook_anarchy = "https://discord.com/api/webhooks/1069654465180881016/QBgsP1x89uPsuPlfdxnKBWu6KMAdlsQ55MKXl_6FcUKPSmtgVrbcmEDyGh5jnAzSKTbl"
webhook_gifts = "https://discord.com/api/webhooks/1069671206678175774/6oC9cFqw-hyBbYkuolhW7eJ_u5qYDbATjHBhK1lCCxZx7vJ86vm91vXqreR4ujrnefru"
webhook_CoinIslandNotif = "https://discord.com/api/webhooks/1069671531539603477/NflDPBF_51vysbpJnyyFXqVP8oApcIAfFjQFvLa8zEKIUVcNLhBTqsviEssNYI1m2Iif"

CoinIsland_roles = {
	0:"discord role ping goes here",
	1:"discord role ping goes here",
	2:"discord role ping goes here",
	3:"discord role ping goes here",
}

badgeDict = {"_1_month" : "<:1month:883780503583465532>","_1_year" : "<:1year:883780503369568277>","_3_months" : "<:3months:883780503440871465>","_admin" : "<:admin:883780503323430933>","_booster" : "<:booster:883780503596060712>","_ppbread" : "<:ppbread:883780503713488916>","_chat_moderator" : "<:chatmoderator:883780503386357781>","_gifter" : "<:gifter:883780503646392370>","_moderator" : "<:moderator:883780503566704710>","_nitro" : "<:nitro:883780503675764736>","_paintingmoderator" : "<:paintingmoderator:883780503151460373>","_paintingowner" : "<:paintingowner:883780503780601866>","_partner" : "<:partner:883780503558299658>","_vip" : "<:vip:883780503516377108>","_former_global_moderator":"<a:formerglobalmoderator:1067942869786169435>","_3_days":"<a:3days:1067947658372730990>"}
gift_items = {1:"Pixel Missile",2:"Pixel Bomb",3:"Atmic Bomb",4:"Premium (1 Month)",5:"Premium (1 Year)",6:"Rainbow Username",7:"Guild Bomb",8:"Avatar Bomb",9:"Name Change",10:"XMAS Username",11:"Premium (3 Days)",12:"HALLOWEEN Username",}

global socketconnection7
socketconnection7 = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
socketconnection7.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
socketconnection7.emit(event='init', data={"authId":"Hawkeye7","boardId":7})
global socketconnection8
socketconnection8 = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
socketconnection8.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
socketconnection8.emit(event='init', data={"authId":"Hawkeye8","boardId":8})
global socketconnection13
socketconnection13 = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
socketconnection13.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
socketconnection13.emit(event='init', data={"authId":"Hawkeye13","boardId":13})

#ill do the new stuff now

global start_time
start_time = datetime.datetime.utcnow()

def background(f):
	'''
	a threading decorator
	use @background above the function you want to run in the background
	'''
	def bg_f(*a, **kw):
		threading.Thread(target=f, args=a, kwargs=kw).start()
	return bg_f

def chat_Safety_Check(data):
	messagetime = datetime.datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
	return messagetime > start_time and data["channel"] in [
		"global",
		"painting",
		"nonenglish",
	]

# Chat Logs

# 7/Global Chat and nonenglish
@socketconnection7.on("chat.user.message")
@background
def logChat7(data):
	# Check if message is new
	if chat_Safety_Check(data) != True:
		return
	# make data easier to use
	messageUsername = data["username"]
	messageChannel = data["channel"]
	messageMention = data["mention"]
	messageGuild = data["guild"]
	messageIcons = data["icons"]
	message = data["message"]
	# handle /here shits
	try:
		x = data["posX"]
		y = data["posY"]
		zoom = data["posS"]
		insert = f"(x:{x},y:{y},zoom:{zoom})"
		message = f"""{message} | /here Coords:{insert}
<https://pixelplace.io/7#x={x}&y={y}&s={zoom}>"""
	except KeyError:
		# There just arent coords / the message doesent include /here
		pass
	except Exception as e:
		print(f"Idk bruh some error somewhere lol ({e})")
		return
	# Convert some shit and get some shit
	discordIconString = getIcons(messageIcons)
	discordRelativeTimestamp = f"Logged <t:{getTimeStamp()}:R>"
	discordGuildNameDivider = "" if messageGuild == "" else " - "
	messageMentionInsert = (f"Mentioned people: {messageMention}" if messageMention != "" else "")
	discordMessage = f"""
{message}
{messageMentionInsert}
"""
	if messageChannel == "global":
		webhookURL = webhook_global
		botUsername = "/7 Chat Message"
		canvas = 7
	elif messageChannel == "nonenglish":
		webhookURL = webhook_nonenglish
		botUsername = "Non english Chat Message"
		canvas = 7
	else:
		print("yo wtf man")
	embed = {"description": f"{discordMessage}","title": f"{messageUsername} {discordIconString}{discordGuildNameDivider}{messageGuild}"}
	whdata = {
		"content": f"{discordRelativeTimestamp}",
		"username": f"{botUsername}",
		"embeds": [embed],
	}
	postWebhook(webhookURL, whdata)
	checkChatMessage(message, messageUsername,canvas)

@socketconnection8.on("chat.user.message")
@background
def logChat8(data):
	# Check if message is new
	if chat_Safety_Check(data) != True:
		return
	# make data easier to use
	messageUsername = data["username"]
	messageChannel = data["channel"]
	messageMention = data["mention"]
	messageGuild = data["guild"]
	messageIcons = data["icons"]
	message = data["message"]
	# return if not 8 message
	if messageChannel != "painting":
		return
	# handle /here shits
	try:
		x = data["posX"]
		y = data["posY"]
		zoom = data["posS"]
		insert = f"(x:{x},y:{y},zoom:{zoom})"
		message = f"""{message} | /here Coords:{insert}
<https://pixelplace.io/8#x={x}&y={y}&s={zoom}>"""
	except KeyError:
		# There just arent coords / the message doesent include /here
		pass
	except Exception as e:
		print(f"Idk bruh some error somewhere lol ({e})")
		return
	# Convert some shit and get some shit
	discordIconString = getIcons(messageIcons)
	discordRelativeTimestamp = f"Logged <t:{getTimeStamp()}:R>"
	discordGuildNameDivider = "" if messageGuild == "" else " - "
	messageMentionInsert = (f"Mentioned people: {messageMention}" if messageMention != "" else "")
	discordMessage = f"""
		{message}
		{messageMentionInsert}
	"""
	embed = {"description": f"{discordMessage}","title": f"{messageUsername} {discordIconString}{discordGuildNameDivider}{messageGuild}"}
	whdata = {
		"content": f"{discordRelativeTimestamp}",
		"username": "/8 Chat Message",
		"embeds": [embed],
	}
	postWebhook(webhook_mvp, whdata)
	checkChatMessage(message, messageUsername,8)

@socketconnection13.on("chat.user.message")
@background
def logChat13(data):
	# Check if message is new
	if chat_Safety_Check(data) != True:
		return
	# make data easier to use
	messageUsername = data["username"]
	messageChannel = data["channel"]
	messageMention = data["mention"]
	messageGuild = data["guild"]
	messageIcons = data["icons"]
	message = data["message"]
	# return if not 13 message
	if messageChannel != "painting":
		return
	# handle /here shits
	try:
		x = data["posX"]
		y = data["posY"]
		zoom = data["posS"]
		insert = f"(x:{x},y:{y},zoom:{zoom})"
		message = f"""{message} | /here Coords:{insert}
<https://pixelplace.io/13#x={x}&y={y}&s={zoom}>"""
	except KeyError:
		# There just arent coords / the message doesent include /here
		pass
	except Exception as e:
		print(f"Idk bruh some error somewhere lol ({e})")
		return
	# Convert some shit and get some shit
	discordIconString = getIcons(messageIcons)
	discordRelativeTimestamp = f"Logged <t:{getTimeStamp()}:R>"
	discordGuildNameDivider = "" if messageGuild == "" else " - "
	messageMentionInsert = (f"Mentioned people: {messageMention}" if messageMention != "" else "")
	discordMessage = f"""
{message}
{messageMentionInsert}
"""
	embed = {"description": f"{discordMessage}","title": f"{messageUsername} {discordIconString}{discordGuildNameDivider}{messageGuild}"}
	whdata = {
		"content": f"{discordRelativeTimestamp}",
		"username": "/13 (/0) Chat Message",   #
		"embeds": [embed],
	}
	postWebhook(webhook_anarchy, whdata)

# Misc Logs

@socketconnection7.on("chat.stats")
@background
def postChatStats(data):
	canvas7Stat = data[0]
	totalStat = data[1]
	content = f"""
Players on Canvas 7>{canvas7Stat}
Players in total   >{totalStat}
These Numbers might not be accurate."""
	embed = {"description": f"{content}","title": "Stats", "color": 16776958} #white
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "Stats","embeds": [embed],}
	postWebhook(webhook_stats, whdata)

@socketconnection7.on("j")
@background
def postJoins(data):
	if data == "":
		return
	content = f"{data} joined!"
	embed = {"description": f"{content}","title": "Joins", "color": 2531122} #green
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "Joins","embeds": [embed],}
	postWebhook(webhook_onoff, whdata)

@socketconnection7.on("l")
@background
def postLeaves(data):
	content = f"{data} left!"
	embed = {"description": f"{content}","title": "Leaves", "color": 13571349} #red
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "Leaves","embeds": [embed],}
	postWebhook(webhook_onoff, whdata)

@socketconnection7.on("chat.system.delete")
@background
def postMutes(data):
	embed = {"description": f"Logged <t:{getTimeStamp()}:R>","title": "Chat Mute detected!", "fields" : [{"name" : "Muted User", "value" : f"{data}"}, {"name" : "Info", "value" : "These logs are not official information. To appeal a mute, join the PixelPlace discord."}], "color": 13036340} #yellow
	whdata = {"content": "","username": "Chat Mutes","embeds": [embed],}
	postWebhook(webhook_mutes, whdata)

@socketconnection7.on("item.notification.gift")
@background
def postGifts(data):
	gifter = data["from"]
	gifted = data["to"]
	item = data["item"]
	gift = gift_items[item]
	embed = {"description": f"Logged <t:{getTimeStamp()}:R>","title": "Gift detected!", "fields" : [{"name" : "Gifted User", "value" : f"{gifted}"}, {"name" : "Gifter", "value" : f"{gifter}"}, {"name" : "Item", "value" : f"{gift}"}], "color": 13036340} #yellow
	whdata = {"content": "","username": "Gift Logs","embeds": [embed],}
	postWebhook(webhook_gifts, whdata)

@socketconnection7.on("coin_island_owner_change")
@background
def postCoinIslandNotif(data):
	newOwner = data["from"]
	coinsGained = data["amount"]
	islandId = data["island"]
	ping = CoinIsland_roles[islandId]
	embed = {"description": f"Logged <t:{getTimeStamp()}:R>","title": f"Coin Island {islandId} has a new Owner", "fields" : [{"name" : "New Owner", "value" : f"{newOwner}"}, {"name" : "Coins gained", "value" : f"{coinsGained}"}], "color": 13036340} #yellow
	whdata = {"content": f"{ping}","username": "Coin Island Logs","embeds": [embed],}
	postWebhook(webhook_CoinIslandNotif, whdata)

# @socketconnection7.on("item.notification.use")
# @background
# def postCoinIslandNotif(data):
# 	newOwner = data["from"]
# 	coinsGained = data["amount"]
# 	islandId = data["island"]
# 	ping = CoinIsland_roles[islandId]
# 	embed = {"description": f"Logged <t:{getTimeStamp()}:R>","title": f"Coin Island {islandId} has a new Owner", "fields" : [{"name" : "New Owner", "value" : f"{newOwner}"}, {"name" : "Coins gained", "value" : f"{coinsGained}"}], "color": 13036340} #yellow
# 	whdata = {"content": f"{ping}","username": "Coin Island Logs","embeds": [embed],}
# 	postWebhook(webhook_CoinIslandNotif, whdata)


# {"userId":37635,"from":"AlmosYT","item":1,"itemName":"Pixel Missile","painting":7,"x":1451,"y":853,"c":38,"zoom":1}]

# 42["areas",[
# {"name":"Australian","state":0,"ownedBy":"Artttt","canvas":55863,"fightEndAt":1675013882,"nextFightAt":0,"fightType":1,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":2120,"yStart":1304,"xEnd":2170,"yEnd":1354,"points":10},
# {"name":"Russian","state":0,"ownedBy":"RDRA","canvas":55940,"fightEndAt":1675007575,"nextFightAt":0,"fightType":0,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":1896,"yStart":446,"xEnd":1946,"yEnd":496,"points":7},
# {"name":"African","state":0,"ownedBy":"FOCF","canvas":41627,"fightEndAt":1675005773,"nextFightAt":0,"fightType":0,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":1244,"yStart":948,"xEnd":1294,"yEnd":998,"points":6},
# {"name":"Antarctica","state":0,"ownedBy":"Thanos69420","canvas":0,"fightEndAt":1675012981,"nextFightAt":0,"fightType":1,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":1308,"yStart":1748,"xEnd":1358,"yEnd":1798,"points":4},
# {"name":"Canadian","state":0,"ownedBy":"Libyanboii","canvas":34493,"fightEndAt":1675008476,"nextFightAt":0,"fightType":1,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":455,"yStart":650,"xEnd":505,"yEnd":700,"points":8},
# {"name":"Brazilian","state":0,"ownedBy":"GRPE","canvas":69696,"fightEndAt":1675014783,"nextFightAt":0,"fightType":0,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":810,"yStart":1190,"xEnd":860,"yEnd":1240,"points":4},
# {"name":"Chinese","state":0,"ownedBy":"Hqjk","canvas":0,"fightEndAt":1675011179,"nextFightAt":0,"fightType":1,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":1902,"yStart":846,"xEnd":1952,"yEnd":896,"points":6},
# {"name":"Greenland","state":0,"ownedBy":"FOCF","canvas":41627,"fightEndAt":1675009377,"nextFightAt":0,"fightType":0,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":870,"yStart":186,"xEnd":920,"yEnd":236,"points":4},
# {"name":"United States","state":0,"ownedBy":"GRPE","canvas":69696,"fightEndAt":1675015684,"nextFightAt":0,"fightType":0,"stats":{},"total":{"guilds":0,"pixels":0,"users":0},"xStart":456,"yStart":810,"xEnd":506,"yEnd":860,"points":12}]]

# 42["area_fight_end",{"id":"7","defended":false,"ownedBy":"GRPE","ownedByGuild":"","previousOwner":"FOCF","fightType":0,"points":4,"stats":[{"guild":"GRPE","pixels":3700,"users":1},{"guild":"HVCD","pixels":2997,"users":1},{"guild":"VOID","pixels":806,"users":1},{"guild":"SCAN","pixels":539,"users":1},{"guild":"TURK","pixels":109,"users":1}],"total":{"guilds":6,"pixels":8161,"users":6},"nextFight":900,"canvas":69696}]

# Helper Methods

def checkChatMessage(message,username,canvas):
	with open(f"{CurrentDir}/filter.txt",'r') as file:
		slurlist = file.read().splitlines()
		for word in message.split():
			if word.lower() in slurlist:
				embed = {"description": f"Logged <t:{getTimeStamp()}:R>","title": "Bad word detected!", "fields" : [{"name" : "Username", "value" : f"{username}"}, {"name" : "Canvas", "value" : f"{canvas}"}, {"name" : "Message", "value" : f"{message}"}, {"name" : "Detected Word", "value" : f"{word}"}], "color": 14662147} #yellow
				whdata = {"content": "","username": "AutoMod","embeds": [embed],}
				postWebhook(webhook_mods, whdata)

def getTimeStamp():
	return str(time.time()).split(".")[0]

def getIcons(icons):
	iconsstr = ""
	for icon in icons:
		icon = icon.replace("-", "_")
		icon = f"_{icon}"
		if icon == "_bread":
			icon = "_ppbread"
		try:
			formatted_icon = badgeDict[f"{icon}"]
		except KeyError:
			print(f"'{icon}' not found")
			continue
		iconsstr = f"{iconsstr}{formatted_icon}"
	return iconsstr

def postWebhook(url, data):
	requests.post(url, json=data)
	time.sleep(1)

while True:
	input("Press Ctrl + c to end")